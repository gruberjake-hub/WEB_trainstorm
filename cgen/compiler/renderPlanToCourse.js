#!/usr/bin/env node

/**
 * renderPlanToCourse.js
 * ---------------------
 * Converts render-plan.json into runtime-ready course.json
 *
 * Usage:
 *   node compiler/renderPlanToCourse.js courses/demo/render-plan.json courses/demo/course.json
 */

const fs = require("fs");
const path = require("path");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf8");
}

function buildCourseMeta(renderPlan) {
  return {
    id: renderPlan.meta.courseId,
    title: renderPlan.meta.title || renderPlan.meta.courseTitle || renderPlan.meta.courseId,
    version: renderPlan.meta.version || "1.0",
    brand: renderPlan.meta.brand || "default",
    theme: renderPlan.meta.theme || "default"
  };
}

function buildNav(scenePlans) {
  return {
    linear: true,
    showProgress: true,
    sceneOrder: scenePlans.map(scene => scene.sceneId)
  };
}

function buildRuntimeComponent(renderUnit) {
  return {
    type: renderUnit.renderType,
    props: renderUnit.props,
    meta: {
      renderUnitId: renderUnit.unitId,
      semanticRole: renderUnit.semanticRole,
      instructionalIntent: renderUnit.instructionalIntent,
      treatment: renderUnit.treatment,
      primitive: renderUnit.primitive,
      styleRef: renderUnit.styleRef,
      sourceElementIds: renderUnit.sourceElementIds
    }
  };
}

function buildVoiceover(scenePlan) {
  if (!scenePlan.narrationPlan || scenePlan.narrationPlan.mode === "none") {
    return null;
  }

  return {
    mode: scenePlan.narrationPlan.mode,
    segments: scenePlan.narrationPlan.segments || []
  };
}

function buildCompletion(scenePlan) {
  return {
    type: scenePlan.completionPlan.completionType,
    requiredUnitIds: scenePlan.completionPlan.requiredUnitIds || [],
    requiredEvents: scenePlan.completionPlan.requiredEvents || []
  };
}

function buildScene(scenePlan) {
  const scene = {
    id: scenePlan.sceneId,
    title: scenePlan.title,
    components: scenePlan.renderUnits.map(buildRuntimeComponent),
    completion: buildCompletion(scenePlan)
  };

  const voiceover = buildVoiceover(scenePlan);
  if (voiceover) {
    scene.voiceover = voiceover;
  }

  return scene;
}

function renderPlanToCourse(renderPlan) {
  return {
    meta: buildCourseMeta(renderPlan),
    nav: buildNav(renderPlan.scenePlans),
    scenes: renderPlan.scenePlans.map(buildScene)
  };
}

function main() {
  const inputPath = process.argv[2];
  const outputPath = process.argv[3] || path.join(path.dirname(inputPath), "course.json");

  if (!inputPath) {
    console.error("Usage: node compiler/renderPlanToCourse.js <inputRenderPlan.json> [outputCourse.json]");
    process.exit(1);
  }

  const renderPlan = readJson(inputPath);
  const course = renderPlanToCourse(renderPlan);
  writeJson(outputPath, course);

  console.log(`Runtime course written to: ${outputPath}`);
}

if (require.main === module) {
  main();
}

module.exports = {
  renderPlanToCourse
};