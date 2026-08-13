# Trainstorm Architectural Rehydration

## 1. Rehydration Metadata

- **Rehydrated at:** 2026-08-13T10:18:04-05:00
- **Source conversation:** `AE Shape Corner Rounding`
- **Source conversation ID:** `69f15e77-d12c-83ea-87c2-d7d74eb4d308`
- **Requested output filename:** `Trainstorm_Rehydration_Untitled_Conversation.md`
- **Scope:** The eight substantive user/assistant exchanges in the source conversation only.
- **Purpose:** Preserve architectural evidence potentially relevant to the system now represented by `trainstorm-core`, especially its transformation of governed learning content into reusable production assets.

## 2. Scope and Evidence Rules

This document is a rehydration, not a claim that every idea in the conversation was implemented. It separates the record into three evidence classes:

- **Explicit user evidence:** A requirement, intention, constraint, or confirmation stated by the user.
- **Assistant proposal:** An architecture, workflow, naming convention, or future direction suggested by the assistant. This is evidence of a discussed design option, not proof of adoption.
- **Derived implication:** A conservative inference from the exchange, labeled as such. It must be validated against the current repository before becoming a requirement.

No external sources, later conversations, repository inspection, or unstated project history are used as evidence here. Product-specific operational claims about After Effects are retained only where they explain the architectural discussion; they are not independently verified in this document.

## 3. Executive Rehydration

The conversation begins as an After Effects technique discussion and develops into a compact architecture for reusable instructional-display primitives. The central pattern is separation of concerns:

1. Course or scene content remains editable as ordinary two-dimensional content.
2. A nested display composition acts as a stable interface between that content and a physical presentation object.
3. A reusable physical primitive—monitor, phone, tablet, laptop, kiosk, or similar—owns geometry, materials, reflections, glow, and other device-specific behavior.
4. The camera and world transform independently from the displayed course content.
5. A scene can be replaced by changing the lowest content reference without rebuilding the enclosing device or final composition.

This is relevant to `trainstorm-core` because it anticipates a renderer-neutral composition model: semantic course scenes are addressable payloads, while presentation primitives are reusable adapters with stable inputs. It also suggests a packaging boundary. An After Effects project does not truly embed its external media; a portable production unit must collect the project and all referenced dependencies into a distributable folder.

The strongest user-confirmed architectural intent is the replaceable nested-content workflow: a 16:9 precomposition is elevated into a 3D scene, and changing the instructional scene occurs in a lower precomposition. The larger primitive library, automatic semantic binding, exposed parameter schema, and project-per-primitive organization were assistant proposals and must not be treated as adopted decisions without validation.

## 4. Conversation Evidence Ledger

### 4.1 Shape geometry and reusable controls

**User evidence**

- The user asked for a convenient way to round rectangle or polygon corners in After Effects and could not find the relevant control surface.

**Assistant proposals and claims**

- Rectangle shapes were described as exposing `Contents → Rectangle 1 → Rectangle Path 1 → Roundness`.
- Polygon, Pen, and converted vector paths were described as lacking the same universal parametric control.
- The `Round Corners` shape operator was proposed for arbitrary paths.
- Illustrator Live Corners were proposed where precision, reuse, or brand consistency matters.
- An expression-driven parametric polygon rig was offered as a possible reusable component with sides, radius, and corner-roundness controls.

**Architectural relevance**

- The exchange distinguishes one-off geometry from reusable, parameterized primitives.
- A production system benefits when visual properties such as corner radius are exposed as governed parameters instead of being baked into manually edited paths.
- **Derived implication:** A rendering schema may need both parametric geometry and freeform-path representations, with explicit validation of which controls each supports.

### 4.2 Flat content in a three-dimensional scene

**User evidence**

- The user asked whether flat footage could track a 3D layer.
- The stated use case involved dual computer monitors, replaceable screen footage, and independent rotation of the overall scene.

**Assistant proposals and claims**

- Three approaches were distinguished: planar corner-pin replacement, camera tracking plus a 3D plane, and a reusable full 3D monitor asset.
- The assistant recommended keeping footage two-dimensional inside a precomposition and making the enclosing screen precomposition a 3D layer.
- The monitor was decomposed into a hierarchy containing bezel, glass/reflection, screen content, glow, and related visual properties.

**Architectural relevance**

- Content payload, device geometry, camera, and world transform are separate concerns.
- The same content can be rebound without reconstructing the scene.
- **Derived implication:** `trainstorm-core` should avoid encoding a course scene as if it were inseparable from a particular device or camera treatment.

### 4.3 Option 3 as a reusable expansion of Option 2

**User evidence**

- The user explicitly characterized the reusable full-scene approach as an expansion of the camera-tracked plane approach: essentially the same process with additional objects representing normal monitor properties.

**Assistant proposals**

- The assistant agreed and characterized the expanded approach as “Option 2 + reusable object-oriented design.”
- A possible object hierarchy was proposed: camera, tracking origin, monitor object, bezel, screen, reflection, shadow, LED glow, and screen-content precomposition.
- A parameter surface was proposed across four groups:
  - Physical: width, height, depth, bezel thickness, corner radius, tilt.
  - Materials: plastic color, metal color, reflection, gloss, screen brightness.
  - Content: source precomposition, scale, crop, safe area.
  - Animation: power on, power off, flicker, glow.
- The assistant proposed a `Screen_Control → Screen_Content_Precomp → Current Scene` indirection so the monitor would not depend on the identity of the displayed scene.
- A future semantic binding was imagined in which a generated `Scene_012` asset automatically binds to `Scene_012_Screen`.

**Architectural relevance**

- This is the clearest expression of a primitive/instance model in the conversation.
- Device behavior is parameterized; scene content is referenced.
- A stable interface can isolate content generation from renderer-specific implementation.
- The semantic binding concept is a proposal, not a confirmed naming contract.

### 4.4 Incremental construction and scene-graph learning

**User evidence**

- The user asked to reach the reusable approach incrementally because of limited confidence in After Effects.
- The user reported a composition containing a 3D object exported from Adobe Dimension and asked whether adding a 3D camera was the next step.

**Assistant proposals and claims**

- The assistant recommended verifying whether the imported object was flat imagery, a Cineware scene, or native 3D geometry before selecting a workflow.
- It proposed creating a camera, testing actual 3D behavior, then aligning a temporary 3D solid as the screen plane before introducing parenting or abstraction.
- The temporary solid was framed as a scaffold for understanding and alignment, not necessarily a production artifact.

**Architectural relevance**

- Complex reusable systems can be introduced through progressively richer valid states.
- **Derived implication:** Authoring and build tooling may benefit from staged validation: verify source type, establish scene/camera validity, align a placeholder, bind content, then package the reusable primitive.

### 4.5 Native 3D model source and composition strategy

**User evidence**

- The user clarified that the monitor was exported from Adobe Dimension as `.gltf`.

**Assistant proposals and claims**

- The assistant treated the `.gltf` as native geometry in After Effects and proposed a camera, multiple views, and a screen plane aligned over the model’s screen.
- A reusable `Monitor_Primitive` composition was proposed containing `Monitor.glTF`, `Screen_PRECOMP`, reflection, emission, and shadow-catcher elements.

**Architectural relevance**

- The physical primitive can depend on external model assets as well as internal composition logic.
- Its dependency manifest therefore needs to represent models, images, footage, and nested project assets—not only textual scene content.

### 4.6 The screen payload is the plane

**User evidence**

- The user identified After Effects version 26 and asked how to map footage onto a solid plane.

**Assistant correction and proposal**

- The assistant clarified that the footage or precomposition itself becomes the 3D plane; the temporary solid is only an alignment aid.
- It proposed a 16:9 precomposition—such as 1600×900 or 1920×1080—made three-dimensional and positioned over the monitor screen.
- It proposed parenting or otherwise coupling the screen plane to the monitor if the monitor itself moves.
- It noted a possible complication if a glTF monitor is imported as a single mesh rather than separately addressable housing, glass, and stand objects.

**Architectural relevance**

- The payload adapter is not a material embedded into the model in this workflow; it is a colocated render layer.
- **Derived implication:** The renderer adapter should state its binding mechanism explicitly. A generic `display_source` relation may compile differently for After Effects, a game engine, or another rendering target.

### 4.7 Confirmed nested replacement workflow

**User evidence**

- The user summarized the intended workflow: take a 16:9 precomposition into the 3D layer and change the underlying footage in a lower precomposition when changing scenes.

**Assistant confirmation and proposals**

- The assistant confirmed the model and described layers of abstraction:
  - main scene and camera;
  - monitor geometry and a 3D display precomposition;
  - display-specific effects;
  - scene precomposition;
  - individual course-scene elements.
- It proposed that monitor-specific effects such as bloom, glow, color correction, vignette, and reflections remain permanently owned by the display layer.
- It proposed semantic naming such as `Monitor_Display` rather than `Screen_PRECOMP`, because “display” describes a stable role rather than current content.
- It imagined generated scene identifiers such as `scene001`, `scene002`, and `scene003` being assigned to device primitives.

**Architectural relevance**

- This exchange supplies the conversation’s strongest confirmed interface boundary.
- The lower scene precomposition is the replaceable payload.
- The display precomposition owns display treatment.
- The device primitive owns physical representation.
- The enclosing scene owns camera, lighting, and spatial composition.

### 4.8 Portability and dependency collection

**User evidence**

- The user asked for an easy way to embed assets in an After Effects project and move the project to another computer.

**Assistant proposals and claims**

- The assistant explained that After Effects projects reference external media rather than truly embedding all assets in the `.aep` file.
- `File → Dependencies → Collect Files` was proposed as the packaging step.
- A collected project was described as a folder containing the project file and copied footage/assets with rewritten paths.
- The assistant proposed organizing a primitive as a project plus assets, compositions, and a demonstration scene.
- It recommended one project per primitive rather than one monolithic library project, with primitives imported into course projects as needed.

**Architectural relevance**

- Portability is a dependency-closure problem, not merely serialization of a project file.
- A production-ready artifact needs a manifest or collection process that captures every externally referenced asset and preserves valid relative relationships.
- Project-per-primitive organization is an assistant recommendation, not a confirmed repository decision.

## 5. Rehydrated Architecture

### 5.1 Layered model

The conversation supports the following renderer-oriented conceptual stack:

```text
Final Scene
├── Camera / lights / world
├── Device Primitive Instance
│   ├── Physical model
│   ├── Device materials and effects
│   └── Display Adapter
│       ├── Display-specific treatment
│       └── Scene Content Reference
│           └── Governed course scene and its elements
└── Other scene objects
```

The first four boundaries map naturally onto a content-production architecture:

| Layer | Responsibility | Expected stability |
|---|---|---|
| Governed scene content | Meaning, instructional sequence, elements, media references | Changes with learning content |
| Scene composition | Turns content into a renderable 16:9 payload | Changes with scene design |
| Display adapter | Fits, crops, masks, and treats the payload for a display surface | Stable across many scenes |
| Device primitive | Geometry, materials, physical properties, device animation | Stable across many courses |
| Final scene | Camera, lighting, environment, timing, spatial arrangement | Changes with production context |

### 5.2 Separation of concerns

The conversation repeatedly separates four independently variable dimensions:

- **Meaning/content:** What the learner sees and hears.
- **Presentation payload:** The composed course scene supplied to a display.
- **Physical primitive:** The monitor or other device that presents it.
- **World/camera:** How the primitive is situated and viewed.

This separation prevents a content edit from forcing reconstruction of the physical scene and prevents a visual device change from rewriting the learning content.

### 5.3 Proposed interface contract

The conversation does not define a formal schema, but it suggests a possible contract that should be treated as a candidate:

```yaml
device_instance:
  primitive_ref: monitor_primitive
  display_source_ref: scene_012
  physical:
    width: null
    height: null
    depth: null
    bezel_thickness: null
    corner_radius: null
    tilt: null
  materials:
    plastic_color: null
    metal_color: null
    reflection: null
    gloss: null
    screen_brightness: null
  content_fit:
    scale: null
    crop: null
    safe_area: null
  animation:
    power_on: null
    power_off: null
    flicker: null
    glow: null
```

This YAML is a derived normalization of an assistant-proposed parameter list. It is not evidence of an existing Trainstorm schema.

## 6. Content Model Implications for `trainstorm-core`

### 6.1 Scene as an addressable payload

The user-confirmed replacement workflow implies that a scene should be independently identifiable and substitutable. A scene identifier should not depend on which monitor, device, or final composition currently renders it.

### 6.2 Primitive as governed reusable definition

A primitive can be understood as a reusable presentation definition with:

- a stable identity;
- an accepted content interface;
- configurable physical, material, fit, and animation parameters;
- renderer-specific assets and implementation;
- versioned dependencies;
- validation rules.

Only the general need for reusable primitives is supported by the conversation. The exact fields above are partly derived from assistant proposals.

### 6.3 Instance as binding

A device instance binds a primitive definition to a scene reference and a set of parameter values. This allows many instances to reuse one definition while displaying different scenes.

### 6.4 Renderer adapter

The After Effects implementation uses nested precompositions and 3D layers. That mechanism should not leak into the semantic content model. A renderer adapter can translate a generic display-source relationship into After Effects project structure, while another adapter could use a material texture, browser surface, or game-engine render target.

### 6.5 Dependency manifest

Because `.aep` projects retain external references, a production unit needs explicit dependency closure. A candidate manifest would record:

- primitive project/version;
- physical model files such as `.gltf`;
- images, audio, video, Illustrator, and Photoshop sources;
- nested compositions or imported projects;
- scene content identifier/version;
- resolved relative package paths;
- integrity or checksum data where supported;
- missing-asset validation status.

Checksums and formal manifests were not discussed explicitly; they are derived governance recommendations prompted by the portability problem.

## 7. Production Pipeline Rehydration

A conservative pipeline inferred from the conversation is:

```text
Governed course scene
        ↓
Renderable 16:9 scene composition
        ↓
Display-source binding
        ↓
Reusable device primitive instance
        ↓
Camera / lighting / final scene composition
        ↓
Dependency collection and validation
        ↓
Portable production package
```

Suggested validation gates:

1. The scene reference resolves to one versioned payload.
2. Payload dimensions/aspect behavior are compatible with the display adapter.
3. Required primitive parameters are valid for the selected renderer.
4. Device and display transforms remain coupled where the device moves.
5. All external dependencies resolve inside the collected package.
6. Reopening the package on a clean environment produces no missing-footage state.

The validation gates are derived recommendations, not explicit commitments in the source conversation.

## 8. Stable Identifiers, Relationships, and Provenance

### 8.1 Identifiers discussed

The assistant used examples including `Scene_012`, `Scene_014`, `scene001`, `Head_01`, and `Image_02`. These demonstrate an assumed semantic-ID direction but do not establish exact case, formatting, uniqueness scope, or lifecycle rules.

### 8.2 Relationships implied

- A final scene **contains** device instances.
- A device instance **instantiates** a primitive definition.
- A device instance or display adapter **references** a scene payload.
- A display adapter **owns** display-specific treatment.
- A primitive definition **depends on** model and visual assets.
- A portable package **collects** the transitive dependency set.

### 8.3 Provenance requirements derived from the exchange

To prevent drift between governed content and production files, a generated scene payload should ideally retain:

- source scene identifier;
- source content version or revision;
- generation timestamp;
- renderer/adapter version;
- primitive identifier/version;
- dependency-package identity;
- build validation result.

These provenance fields are not stated in the conversation; they are derived safeguards relevant to `trainstorm-core`.

## 9. Governance and Drift Prevention

The conversation’s nested replacement model creates a useful governance boundary: course content changes below the display interface, while reusable presentation behavior remains above it. To preserve that boundary:

- Device effects should not contain ungoverned instructional meaning.
- Scene content should not hard-code a particular device unless the learning requirement demands it.
- Stable references should replace manual relinking where feasible.
- Primitive revisions should be versioned so a library improvement does not silently alter already approved productions.
- Packaging should capture exact dependencies rather than whichever library files happen to be current on another computer.
- Renderer-specific naming should be mapped from semantic identifiers, not treated as the source of truth.

All bullets in this section are derived governance implications. The conversation motivates them but does not record their adoption.

## 10. Decisions, Proposals, and Unresolved Status

### 10.1 User-confirmed or user-stated direction

- Flat instructional footage needs to appear on monitors in a 3D After Effects scene.
- Screen content should be swappable independently of the wider scene.
- The scene should be rotatable independently from the screen payload.
- The working 3D asset came from Adobe Dimension as `.gltf`.
- The working After Effects environment was identified as version 26.
- The intended composition pattern uses a 16:9 precomposition in 3D and replaces content in a lower precomposition.
- The production asset needs to be transferable to another computer.

### 10.2 Assistant proposals requiring repository validation

- A reusable `Monitor_Primitive` and wider device-primitive library.
- A dedicated `Monitor_Display` abstraction.
- A `Screen_Control → Screen_Content_Precomp → Current Scene` chain.
- Automatic binding from semantic scene IDs to renderer assets.
- The listed physical, material, content-fit, and animation parameters.
- One After Effects project per primitive.
- Device-specific effects permanently owned by the display composition.

### 10.3 Unresolved questions

- Are device primitives represented in the current `trainstorm-core` ontology or only in downstream rendering code?
- What is the canonical scene-ID syntax and uniqueness scope?
- Is a display source a direct scene reference, a render artifact reference, or a versioned binding entity?
- Which properties belong to the semantic model, the design system, the renderer adapter, and the individual instance?
- How are primitive updates propagated without changing approved outputs unexpectedly?
- Does the build system generate After Effects structures, populate templates, or only emit renderer-neutral manifests?
- What is the canonical portable-package format and validation process?
- How are fonts, plug-ins, color profiles, and other environmental dependencies represented, since the conversation focused primarily on collected media?

## 11. Risks and Tensions

### 11.1 Semantic naming versus renderer naming

Names such as `Monitor_Display` are clearer than generic implementation labels, but After Effects composition names are still renderer-local. Treating them as canonical semantic identifiers would couple governance to one tool.

### 11.2 Library reuse versus reproducibility

Importing improved primitives from a shared library promotes reuse, but automatically adopting the latest primitive can change an approved course. Version pinning is needed if reproducibility matters.

### 11.3 Project-per-primitive versus operational overhead

Separate primitive projects can reduce monolithic complexity, but they also multiply dependency, version, and import-management concerns. The appropriate granularity needs evidence from current production volume and tooling.

### 11.4 Flexible screen content versus aspect mismatch

A generic display can accept videos, browser mockups, dashboards, or course scenes, but their aspect ratios and safe areas may differ. Content-fit behavior must be explicit rather than inferred manually.

### 11.5 Single-mesh models versus bindable surfaces

If imported geometry does not expose the screen as a distinct object or anchor, screen alignment can become fragile. Primitive asset specifications may need named anchors, separated meshes, or renderer-specific alignment metadata.

## 12. Recommended Repository Reconciliation

The following are reconciliation tasks, not claims about the current repository:

1. Search the current schema and registries for concepts equivalent to `scene`, `primitive`, `primitive_instance`, `display_adapter`, `render_artifact`, and `dependency_package`.
2. Map existing identifiers to the relationships recovered here without adopting the conversation’s example names blindly.
3. Determine whether the renderer boundary already isolates After Effects-specific concepts such as compositions, layers, cameras, and collected projects.
4. Add or confirm validation for content-reference resolution, parameter compatibility, dependency closure, and version pinning.
5. Record any deliberate conflict between the current architecture and the assistant proposals in this conversation.
6. If a monitor primitive already exists, test the user-confirmed operation: replace the lower scene payload without editing device geometry or final-scene structure.

## 13. Compact Architectural Record

### Problem

Reusable instructional scenes need to appear on physical display objects in a 3D motion environment, while content, device appearance, and camera/world motion remain independently changeable and the resulting project remains portable.

### Confirmed workflow intent

Use a nested 16:9 content composition as the swappable payload of a 3D display layer; change the lower scene composition rather than rebuilding the device or enclosing scene.

### Candidate architectural pattern

Represent governed scenes as stable references, bind them through a display adapter to versioned device-primitive instances, and package the complete renderer dependency graph for delivery.

### Architectural value

The pattern promotes reuse, reduces manual scene rebuilding, separates instructional meaning from physical presentation, supports renderer adapters, and creates clear boundaries for validation, provenance, and version governance.

### Evidence caveat

Only the user-stated needs and confirmations are authoritative conversation evidence. Most formal schema, automation, versioning, manifest, and governance details in this rehydration are derived implications that require reconciliation with `trainstorm-core`.

