#!/usr/bin/env node

/**
 * Trainstorm v1 Planner
 * ---------------------
 * Converts a semantic course JSON into a render-plan JSON.
 *
 * Usage:
 *   node planner/planCourse.js courses/demo/course.semantic.json courses/demo/render-plan.json
 *
 * If no output path is provided, defaults to:
 *   <inputDir>/render-plan.json
 *
 * Assumptions about semantic input:
 * - top-level object with optional `meta`
 * - scenes in `scenes`
 * - each scene may contain semantic elements in one of:
 *   - scene.elements
 *   - scene.content
 *   - scene.children
 *   - scene.nodes
 *
 * Supported semantic roles:
 *   Module, Scene, Content, Head, SubHead, ContentHead, ListHead, List,
 *   Bullet, Statement, Paragraph, Impact, Quote
 *
 * This planner is intentionally deterministic and conservative.
 * It creates a usable planning artifact first; richer intelligence can be layered later.
 */

const fs = require("fs");
const path = require("path");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf8");
}

function ensureArray(value) {
  if (Array.isArray(value)) return value;
  if (value == null) return [];
  return [value];
}

function slugify(value) {
  return String(value || "")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "") || "item";
}

function firstNonEmpty(...values) {
  for (const v of values) {
    if (typeof v === "string" && v.trim()) return v.trim();
  }
  return "";
}

function getSceneElements(scene) {
  return ensureArray(
    scene.elements ??
      scene.content ??
      scene.children ??
      scene.nodes ??
      []
  );
}

function safeId(prefix, value, fallbackIndex) {
  const raw = firstNonEmpty(value);
  return raw ? raw : `${prefix}_${fallbackIndex + 1}`;
}

function inferCourseMeta(semanticCourse, inputPath) {
  const inputBase = path.basename(inputPath, path.extname(inputPath));
  const courseId =
    semanticCourse?.meta?.courseId ||
    semanticCourse?.id ||
    semanticCourse?.courseId ||
    inputBase;

  return {
    courseId,
    version: semanticCourse?.meta?.version || "1.0",
    plannerVersion: "0.1",
    sourceSemanticFile: path.basename(inputPath),
    brand: semanticCourse?.meta?.brand || "default",
    theme: semanticCourse?.meta?.theme || "default",
    generatedAt: new Date().toISOString()
  };
}
function getSceneSignals(scene) {
  const elements = getSceneElements(scene).filter(Boolean);

  const listElements = elements.filter(el => el.type === "List");
  const mcqElements = elements.filter(el => el.type === "MCQ");
  const impactElements = elements.filter(el => el.type === "Impact");
  const headingElements = elements.filter(el => el.type === "Head");
  const paragraphElements = elements.filter(el => el.type === "Paragraph");
  const statementElements = elements.filter(el => el.type === "Statement");

  const totalListItems = listElements.reduce((sum, el) => {
    return sum + ((el.items && el.items.length) || 0);
  }, 0);

  const textLikeCount =
    headingElements.length +
    paragraphElements.length +
    statementElements.length +
    impactElements.length;

  const isSparse = elements.length <= 2 && textLikeCount <= 2;
  const hasMCQ = mcqElements.length > 0;
  const hasImpact = impactElements.length > 0;
  const hasList = listElements.length > 0;
  const hasLongList = totalListItems >= 3;

  const hasContrastSignals =
    elements.length === 2 &&
    (
      statementElements.length === 2 ||
      impactElements.length === 2
    );

  return {
    elementCount: elements.length,
    hasMCQ,
    hasImpact,
    hasList,
    hasLongList,
    isSparse,
    hasContrastSignals
  };
}

const SCENE_TREATMENTS = {
  DIDACTIC_FLOW: "didactic-flow",
  EMPHASIS_FRAME: "emphasis-frame",
  PROGRESSIVE_REVEAL: "progressive-reveal",
  CONTRAST_FRAME: "contrast-frame",
  ASSESSMENT_BEAT: "assessment-beat"
};

const UNIT_TREATMENTS = {
  PRIMARY_ASSERTION: "primary-assertion",
  SUPPORTING_CONTEXT: "supporting-context",
  EMPHASIS_BEAT: "emphasis-beat",
  PROGRESSIVE_STEP: "progressive-step",
  CONTRAST_PAIR: "contrast-pair",
  INTERACTION_PROMPT: "interaction-prompt"
};

function assignSceneTreatment(scene, signals) {
  if (signals.hasMCQ) {
    return SCENE_TREATMENTS.ASSESSMENT_BEAT;
  }

  if (signals.hasImpact && signals.isSparse) {
    return SCENE_TREATMENTS.EMPHASIS_FRAME;
  }

  if (signals.hasList && signals.hasLongList) {
    return SCENE_TREATMENTS.PROGRESSIVE_REVEAL;
  }

  if (signals.hasContrastSignals) {
    return SCENE_TREATMENTS.CONTRAST_FRAME;
  }

  return SCENE_TREATMENTS.DIDACTIC_FLOW;
}

function assignUnitTreatment(unit, sceneTreatment) {
  const unitType = unit.semanticRole || unit.semanticType || unit.type;

  if (unitType === "Head") {
    return UNIT_TREATMENTS.PRIMARY_ASSERTION;
  }

  if (unitType === "Impact") {
    return UNIT_TREATMENTS.EMPHASIS_BEAT;
  }

  if (unitType === "MCQ") {
    return UNIT_TREATMENTS.INTERACTION_PROMPT;
  }

  if (sceneTreatment === SCENE_TREATMENTS.PROGRESSIVE_REVEAL) {
    if (unitType === "List" || unitType === "Statement" || unitType === "Paragraph") {
      return UNIT_TREATMENTS.PROGRESSIVE_STEP;
    }
  }

  if (sceneTreatment === SCENE_TREATMENTS.CONTRAST_FRAME) {
    if (unitType === "Statement" || unitType === "Impact" || unitType === "Paragraph") {
      return UNIT_TREATMENTS.CONTRAST_PAIR;
    }
  }

  return UNIT_TREATMENTS.SUPPORTING_CONTEXT;
}
function inferGlobalDirectives(semanticCourse) {
  return {
    density: semanticCourse?.meta?.density || "medium",
    tone: semanticCourse?.meta?.tone || "clear-confident-human",
    visualStyle: semanticCourse?.meta?.visualStyle || "clean-didactic",
    narrationMode: semanticCourse?.meta?.narrationMode || "scene-based",
    motionMode: semanticCourse?.meta?.motionMode || "hybrid",
    interactionMode: semanticCourse?.meta?.interactionMode || "light"
  };
}

function inferSceneIntent(scene, elements) {
  const explicit = scene.sceneIntent || scene.intent;
  if (explicit) return explicit;

  const hasCheck = elements.some((el) => {
    const t = el.type || el.semanticRole;
    return t === "MCQ" || t === "KnowledgeCheck" || el.intent === "check";
  });
  if (hasCheck) return "check";

  const hasImpact = elements.some((el) => (el.type || el.semanticRole) === "Impact");
  if (hasImpact) return "persuade";

  const hasQuote = elements.some((el) => (el.type || el.semanticRole) === "Quote");
  if (hasQuote) return "contextualize";

  return "explain";
}

function inferLearningRole(scene, elements) {
  if (scene.learningRole) return scene.learningRole;

  const hasCheck = elements.some((el) => {
    const t = el.type || el.semanticRole;
    return t === "MCQ" || t === "KnowledgeCheck" || el.intent === "check";
  });
  if (hasCheck) return "knowledge-check";

  const hasImpact = elements.some((el) => (el.type || el.semanticRole) === "Impact");
  if (hasImpact) return "concept-development";

  return "concept-introduction";
}

function inferExperienceStrategy(sceneIntent, learningRole, elements) {
  const hasList = elements.some((el) => (el.type || el.semanticRole) === "List");
  const hasCheck = learningRole === "knowledge-check";
  const hasImpact = elements.some((el) => (el.type || el.semanticRole) === "Impact");

  let primaryMove = "explain";
  if (hasCheck) primaryMove = "test_understanding";
  else if (hasList) primaryMove = "progressive_reveal";
  else if (hasImpact) primaryMove = "explain_then_emphasize";
  else if (sceneIntent === "orient") primaryMove = "orient";
  else if (sceneIntent === "contextualize") primaryMove = "contextualize";

  let interactionPattern = "passive";
  if (hasCheck) interactionPattern = "knowledge-check";
  else if (hasList) interactionPattern = "progressive-disclosure";

  return {
    primaryMove,
    secondaryMoves: dedupe([
      sceneIntent === "orient" ? "anchor" : null,
      hasImpact ? "emphasize" : null,
      hasList ? "clarify" : null
    ]),
    pacing: hasCheck ? "moderate" : "moderate",
    interactionPattern,
    visualDensity: hasList ? "medium" : "light",
    narrativeEnergy: hasImpact ? "elevated" : "measured"
  };
}

function dedupe(arr) {
  return [...new Set(arr.filter(Boolean))];
}

function normalizeSemanticType(el) {
  return (
    el.semanticRole ||
    el.type ||
    inferTypeFromShape(el) ||
    "Paragraph"
  );
}

function inferTypeFromShape(el) {
  if (el.items && Array.isArray(el.items)) return "List";
  if (el.choices || el.options) return "MCQ";
  if (el.quote || el.attribution) return "Quote";
  return null;
}

function normalizeIntent(el, semanticType) {
  return (
    el.intent ||
    ({
      Head: "orient",
      SubHead: "refine",
      ContentHead: "refine",
      ListHead: "organize",
      List: "structure",
      Bullet: "specify",
      Statement: "assert",
      Paragraph: "explain",
      Impact: "persuade",
      Quote: "contextualize",
      MCQ: "check",
      Content: "organize",
      Scene: "transition",
      Module: "orient"
    }[semanticType] || "explain")
  );
}

function normalizeImportance(el, semanticType) {
  return (
    el.importance ||
    ({
      Head: "high",
      Impact: "high",
      MCQ: "high",
      SubHead: "medium",
      ContentHead: "medium",
      ListHead: "medium",
      List: "medium",
      Quote: "medium",
      Paragraph: "medium",
      Statement: "medium",
      Bullet: "low"
    }[semanticType] || "medium")
  );
}

function toSourceElement(el, idx) {
  const semanticType = normalizeSemanticType(el);
  const intent = normalizeIntent(el, semanticType);
  const importance = normalizeImportance(el, semanticType);

  return {
    elementId: safeId("el", el.id, idx),
    type: semanticType,
    intent,
    importance,
    ...(el.notes ? { notes: el.notes } : {})
  };
}

function planningAttrsForSemanticType(semanticRole) {
  switch (semanticRole) {
    case "Head":
      return {
        instructionalIntent: "orient",
        rhetoricalWeight: "high",
        rhetoricalTreatment: "summary-highlight",
        learnerAction: "notice"
      };
    case "SubHead":
    case "ContentHead":
    case "ListHead":
      return {
        instructionalIntent: "refine",
        rhetoricalWeight: "medium",
        rhetoricalTreatment: "supporting-detail",
        learnerAction: "read"
      };
    case "Statement":
      return {
        instructionalIntent: "assert",
        rhetoricalWeight: "medium",
        rhetoricalTreatment: "emphasized-assertion",
        learnerAction: "consider"
      };
    case "Paragraph":
      return {
        instructionalIntent: "explain",
        rhetoricalWeight: "medium",
        rhetoricalTreatment: "plain-exposition",
        learnerAction: "read"
      };
    case "Impact":
      return {
        instructionalIntent: "persuade",
        rhetoricalWeight: "high",
        rhetoricalTreatment: "emphasized-assertion",
        learnerAction: "retain"
      };
    case "Quote":
      return {
        instructionalIntent: "contextualize",
        rhetoricalWeight: "medium",
        rhetoricalTreatment: "framed-quote",
        learnerAction: "consider"
      };
    case "List":
      return {
        instructionalIntent: "structure",
        rhetoricalWeight: "medium",
        rhetoricalTreatment: "progressive-reveal",
        learnerAction: "explore"
      };
    case "MCQ":
      return {
        instructionalIntent: "check",
        rhetoricalWeight: "high",
        rhetoricalTreatment: "knowledge-check",
        learnerAction: "respond"
      };
    default:
      return {
        instructionalIntent: "explain",
        rhetoricalWeight: "medium",
        rhetoricalTreatment: "plain-exposition",
        learnerAction: "read"
      };
  }
}

function renderRoleForSemanticType(semanticRole) {
  switch (semanticRole) {
    case "Head":
      return "headline";
    case "SubHead":
    case "ContentHead":
    case "ListHead":
      return "subheadline";
    case "Impact":
      return "emphasis";
    case "Quote":
      return "quote";
    case "List":
      return "reveal-set";
    case "Statement":
      return "supporting-detail";
    case "MCQ":
      return "knowledge-check";
    default:
      return "exposition";
  }
}

function styleRefForSemanticType(semanticRole) {
  switch (semanticRole) {
    case "Head":
      return "head-primary";
    case "SubHead":
      return "subhead-secondary";
    case "ContentHead":
      return "content-head";
    case "ListHead":
      return "list-head";
    case "List":
      return "list-body";
    case "Impact":
      return "impact-emphasis";
    case "Quote":
      return "quote-context";
    case "MCQ":
      return "knowledge-check";
    default:
      return "content-body";
  }
}

function primitiveForSemanticType(semanticRole) {
  switch (semanticRole) {
    case "Head":
      return "StaticHead";
    case "SubHead":
    case "ContentHead":
      return "LineReveal";
    case "ListHead":
      return "LineReveal";
    case "Paragraph":
      return "BodyFade";
    case "Statement":
      return "BodyFade";
    case "Impact":
      return "FocusReveal";
    case "Quote":
      return "QuoteFade";
    case "List":
      return "CardReveal";
    case "MCQ":
      return "KnowledgeCheck";
    default:
      return "BodyFade";
  }
}

function renderTypeForSemanticType(semanticRole, el) {
  if (semanticRole === "List") return "RevealCards";
  if (semanticRole === "Head" || semanticRole === "SubHead" || semanticRole === "ContentHead" || semanticRole === "ListHead" || semanticRole === "Impact") {
    return "Heading";
  }
  if (semanticRole === "MCQ" || el.choices || el.options) return "MCQ";
  return "Body";
}

function textFromElement(el) {
  return firstNonEmpty(
    el.text,
    el.body,
    el.content,
    el.label,
    el.quote,
    el.statement,
    el.paragraph
  );
}

function toHeadingProps(el, semanticRole) {
  const level =
    semanticRole === "Head"
      ? 2
      : semanticRole === "Impact"
      ? 3
      : 3;

  return {
    level,
    text: textFromElement(el)
  };
}

function toBodyProps(el, semanticRole) {
  const emphasis =
    semanticRole === "Impact"
      ? "high"
      : semanticRole === "Statement"
      ? "medium"
      : "none";

  return {
    text: textFromElement(el),
    emphasis,
    role: semanticRole
  };
}

function toRevealCardsProps(el, unitId) {
  const items = ensureArray(el.items).map((item, idx) => ({
    id: item.id || `${unitId}_item_${idx + 1}`,
    title: firstNonEmpty(item.title, item.head, item.label, `Item ${idx + 1}`),
    body: firstNonEmpty(item.body, item.text, item.content, item.description, "...")
  }));

  return {
    id: el.id || unitId,
    items,
    requireAllRevealedToComplete: true
  };
}

function toMcqProps(el, unitId) {
  const options = ensureArray(el.options ?? el.choices).map((choice, idx) => ({
    id: choice.id || `choice_${idx + 1}`,
    text: firstNonEmpty(choice.text, choice.label, choice.body, `Choice ${idx + 1}`),
    correct: Boolean(choice.correct),
    ...(choice.rationale ? { rationale: choice.rationale } : {})
  }));

  return {
    id: el.id || unitId,
    question: firstNonEmpty(el.question, el.stem, el.prompt, el.text, "Choose the best answer."),
    options,
    feedback: {
      correct: el.feedback?.correct || "Correct.",
      incorrect: el.feedback?.incorrect || "Try again."
    },
    retry: {
      allowed: el.retry?.allowed ?? true
    }
  };
}

function buildRenderUnit(el, idx, sceneId) {
  const semanticRole = normalizeSemanticType(el);
  const renderType = renderTypeForSemanticType(semanticRole, el);
  const attrs = planningAttrsForSemanticType(semanticRole);
  const visualIntent = visualIntentForSemanticType(semanticRole);
  const unitId = el.unitId || `${sceneId}_u${idx + 1}`;
  const sourceElementId = safeId("el", el.id, idx);

  let props;
  if (renderType === "Heading") {
    props = toHeadingProps(el, semanticRole);
  } else if (renderType === "RevealCards") {
    props = toRevealCardsProps(el, unitId);
  } else if (renderType === "MCQ") {
    props = toMcqProps(el, unitId);
  } else {
    props = toBodyProps(el, semanticRole);
  }

  return {
    unitId,
    semanticRole,
    instructionalIntent: attrs.instructionalIntent,
    rhetoricalWeight: attrs.rhetoricalWeight,
    rhetoricalTreatment: attrs.rhetoricalTreatment,
    learnerAction: attrs.learnerAction,
    role: renderRoleForSemanticType(semanticRole),
    sourceElementIds: [sourceElementId],
    renderType,
    props,
    styleRef: styleRefForSemanticType(semanticRole),
    primitive: primitiveForSemanticType(semanticRole),
    importance: normalizeImportance(el, semanticRole),
    visualIntent,
    ...(el.notes ? { notes: el.notes } : {})
  };
}

function estimateDurationMs(text) {
  const words = String(text || "").trim().split(/\s+/).filter(Boolean).length;
  if (words === 0) return 0;
  const wordsPerMinute = 145;
  const minutes = words / wordsPerMinute;
  return Math.max(1200, Math.round(minutes * 60 * 1000));
}

function buildNarrationPlan(scenePlan) {
  const narratableUnits = scenePlan.renderUnits.filter((u) => {
    if (u.renderType === "MCQ") return false;
    if (u.renderType === "RevealCards") return false;
    const text = u.props?.text;
    return typeof text === "string" && text.trim().length > 0;
  });

  const segments = narratableUnits.map((unit, idx) => {
    const text = unit.props.text;
    return {
      segmentId: `${scenePlan.sceneId}_n${idx + 1}`,
      sourceUnitIds: [unit.unitId],
      text,
      voiceStyle:
        unit.semanticRole === "Impact"
          ? "slight-emphasis"
          : unit.semanticRole === "Head"
          ? "clear-warm"
          : "clear-neutral",
    timing: {
        ...(idx > 0 ? { startAfterUnit: narratableUnits[idx - 1].unitId } : {}),
        estimatedDurationMs: estimateDurationMs(text)
      }
    };
  });

  return {
    mode: segments.length ? "scene-based" : "none",
    segments
  };
}

function buildMotionPlan(scenePlan) {
  const units = scenePlan.renderUnits.map((unit) => ({
    unitId: unit.unitId,
    motionPrimitive: unit.primitive,
    aeEligible: ["FocusReveal", "GlassReveal", "LineReveal", "BulletReveal", "QuoteFade"].includes(unit.primitive),
    ...(["FocusReveal", "QuoteFade"].includes(unit.primitive)
      ? { aeTemplate: templateForPrimitive(unit.primitive) }
      : {})
  }));

  return {
    mode: units.some((u) => u.aeEligible) ? "hybrid" : "html-only",
    units
  };
}

function templateForPrimitive(primitive) {
  switch (primitive) {
    case "FocusReveal":
      return "impact_focus_reveal";
    case "QuoteFade":
      return "quote_fade";
    case "LineReveal":
      return "line_reveal";
    case "BulletReveal":
      return "bullet_reveal";
    default:
      return "default";
  }
}

function buildCompletionPlan(scenePlan) {
  const revealUnits = scenePlan.renderUnits.filter((u) => u.renderType === "RevealCards");
  const mcqUnits = scenePlan.renderUnits.filter((u) => u.renderType === "MCQ");

  const requiredEvents = [
    ...revealUnits.map((u) => ({
      event: "REVEALCARDS_COMPLETE",
      id: u.props.id || u.unitId
    })),
    ...mcqUnits.map((u) => ({
      event: "MCQ_ANSWERED",
      id: u.props.id || u.unitId
    }))
  ];

  return {
    completionType: requiredEvents.length ? "event-based" : "view",
    requiredUnitIds: [],
    requiredEvents
  };
}

function buildLearnerOutcome(scene, sceneIntent, renderUnits) {
  if (scene.learnerOutcome) return scene.learnerOutcome;

  const headline = renderUnits.find((u) => u.role === "headline")?.props?.text;
  const emphasis = renderUnits.find((u) => u.role === "emphasis")?.props?.text;

  if (sceneIntent === "check") {
    return "Learner can respond correctly to the knowledge check for this scene.";
  }

  if (headline && emphasis) {
    return `Learner understands "${headline}" and retains the key point that ${stripTerminalPunctuation(emphasis).toLowerCase()}.`;
  }

  if (headline) {
    return `Learner understands the core idea of "${headline}".`;
  }

  return "Learner understands the central point of this scene.";
}

function stripTerminalPunctuation(text) {
  return String(text || "").replace(/[.!?]+$/, "");
}

function buildScenePlan(scene, sceneIndex) {
  const sceneId = safeId("s", scene.id, sceneIndex);
  const rawElements = getSceneElements(scene);
  const normalizedElements = rawElements.filter(Boolean);

  const sourceElements = normalizedElements.map(toSourceElement);
  const sceneIntent = inferSceneIntent(scene, normalizedElements);
  const learningRole = inferLearningRole(scene, normalizedElements);

  const sceneSignals = getSceneSignals(scene);
  const sceneTreatment = assignSceneTreatment(scene, sceneSignals);

  const renderUnits = normalizedElements.map((el, idx) => {
    const unit = buildRenderUnit(el, idx, sceneId);
    unit.unitTreatment = assignUnitTreatment(unit, sceneTreatment);
    return unit;
  });

  const scenePlan = {
    sceneId,
    sceneIntent,
    title: firstNonEmpty(scene.title, scene.name, `Scene ${sceneIndex + 1}`),
    learningRole,
    learnerOutcome: "",

    sceneSignals,
    sceneTreatment,

    experienceStrategy: inferExperienceStrategy(sceneIntent, learningRole, normalizedElements),
    sourceElements,
    renderUnits,
    narrationPlan: { mode: "none", segments: [] },
    motionPlan: { mode: "none", units: [] },
    completionPlan: { completionType: "view", requiredUnitIds: [], requiredEvents: [] }
  };

  scenePlan.learnerOutcome = buildLearnerOutcome(scene, sceneIntent, renderUnits);
  scenePlan.narrationPlan = buildNarrationPlan(scenePlan);
  scenePlan.motionPlan = buildMotionPlan(scenePlan);
  scenePlan.completionPlan = buildCompletionPlan(scenePlan);

  return scenePlan;

}

function planCourse(semanticCourse, inputPath) {
  const scenes = ensureArray(semanticCourse.scenes);

  if (!scenes.length) {
    throw new Error("Semantic course contains no scenes.");
  }

  return {
    meta: inferCourseMeta(semanticCourse, inputPath),
    globalDirectives: inferGlobalDirectives(semanticCourse),
    scenePlans: scenes.map(buildScenePlan)
  };
}

function resolveOutputPath(inputPath, outputArg) {
  if (outputArg) return outputArg;
  return path.join(path.dirname(inputPath), "render-plan.json");
}

function main() {
  const inputPath = process.argv[2];
  const outputPath = resolveOutputPath(inputPath, process.argv[3]);

  if (!inputPath) {
    console.error("Usage: node planner/planCourse.js <inputSemanticCourse.json> [outputRenderPlan.json]");
    process.exit(1);
  }

  const semanticCourse = readJson(inputPath);
  const renderPlan = planCourse(semanticCourse, inputPath);

  writeJson(outputPath, renderPlan);

  console.log(`Render plan written to: ${outputPath}`);
}

if (require.main === module) {
  main();
}

function visualIntentForSemanticType(semanticRole) {
  switch (semanticRole) {
    case "Head":
      return {
        supportLevel: "light",
        visualRole: "none",
        treatmentHint: "text-only"
      };
    case "SubHead":
    case "ContentHead":
    case "ListHead":
      return {
        supportLevel: "light",
        visualRole: "organizational",
        treatmentHint: "icon-support"
      };
    case "Paragraph":
      return {
        supportLevel: "none",
        visualRole: "none",
        treatmentHint: "text-only"
      };
    case "Statement":
      return {
        supportLevel: "light",
        visualRole: "contrast",
        treatmentHint: "contrast-layout"
      };
    case "Impact":
      return {
        supportLevel: "medium",
        visualRole: "emphasis",
        treatmentHint: "hero-visual"
      };
    case "Quote":
      return {
        supportLevel: "light",
        visualRole: "contextual",
        treatmentHint: "supporting-image"
      };
    case "List":
      return {
        supportLevel: "high",
        visualRole: "organizational",
        treatmentHint: "structured-cards"
      };
    case "MCQ":
      return {
        supportLevel: "light",
        visualRole: "organizational",
        treatmentHint: "text-only"
      };
    default:
      return {
        supportLevel: "none",
        visualRole: "none",
        treatmentHint: "text-only"
      };
  }
}
module.exports = {
  planCourse
};