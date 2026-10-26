```markdown
# SYSTEM SKILL: UNITY TERRAIN CREATION & LEVEL DESIGN (URP)

## 1. BASE ELEVATION & SCULPTING CONTROLS

### 1.1 Baseline Elevation Management
* **Negative Elevation Constraint**: Unity terrain cannot be sculpted below world level 0 by default.
* **Flatten Tile Protocol**: Before starting any sculpting, select the **Paint Terrain** tab, choose the **Set Height** tool, specify a baseline height offset, and click **Flatten Tile**. This elevates the base floor, allowing rivers, valleys, and pits to be carved below the initial surface level.

### 1.2 Height Bounds & Resolution Scaling
* **Max Height Limit**: Define the maximum **Terrain Height** parameter in **Terrain Options** before sculpting. Unity caps maximum mesh elevation to this specified value.
* **16-Bit Depth Brushes**: Use 16-bit depth brush masks to eliminate staircasing artifacts during sculpting.
* **Non-Destructive Scaling**: Heightmap smoothing correlates directly with resolution—higher resolutions yield finer detail and less smoothing. You can safely scale **Heightmap Resolution** upward during production without losing existing sculpted contours. Downward scaling destroys height data and is prohibited.

### 1.3 Precision Sculpting Tools
* **Elevation Sampling (`Shift + Click`)**: When using the **Set Height** tool, hold `Shift` and click anywhere on the terrain to instantly sample and lock that precise elevation value into the tool.
* **Relative Stamp Offset (`Max Add = 1`)**: When applying stamps, set `Max Add` to `1`. A value of `0` measures stamp height from world zero, whereas `1` offsets stamp height relative to the current local terrain surface.
* **Build Persistence for Terrain Holes**: When using the **Paint Holes** tool, enable **Terrain Hole** under **Project Settings**. If disabled, holes will appear solid in standalone game builds.

---

## 2. REALISTIC HEIGHT-BASED TERRAIN LAYER BLENDING

### 2.1 Mask Map RGBA Channel Specification
Unity HDRP `TerrainLit` shaders read surface properties encoded across the RGBA channels of a Mask Map:
* **Red Channel**: Metallic Map (`0` = non-metallic, `1` = metallic).
* **Green Channel**: Ambient Occlusion Map.
* **Blue Channel**: Height Map (`1` / White = high peaks/stones; `0` / Dark = low crevices/soil).
* **Alpha Channel**: Smoothness Map (`0` = rough/matte, `1` = smooth/reflective).

### 2.2 Texture Height Encoding Workflow
If source textures lack height data in the blue channel, prepare them in a graphics editor:
1. Open the **Diffuse (Albedo)** texture and the target **Mask Map**.
2. **Desaturate** the Diffuse texture.
3. Boost shadow, midtone, and highlight contrast so raised surface features become light/white.
4. Copy the contrasted image, select the **Blue Channel** of the Mask Map, and paste it.
5. Select all channels and export as a 32-bit `TIFF` or `Targa` file.

### 2.3 HDRP Material & Remapping Setup
1. Create a material using the **HDRP / TerrainLit** shader.
2. Enable **Height-based Blending**, set a slight **Height Transition** offset, and check **GPU Instancing**.
3. Assign the material to the Terrain's **Material** slot.
4. In each Terrain Layer's inspector, configure **Channel Remapping**:
   * Set **Amplitude** to `100` across all layers.
   * Tune the **Base** slider to set relative layer hierarchy (e.g., determining whether sand sits above or below stone).
5. **Painting Rule**: Avoid hard texture cut-offs; blend layer boundaries gradually so high-elevation details (peaks) emerge through low crevices first.

---

## 3. FOLIAGE, VEGETATION & DETAIL OPTIMIZATION

### 3.1 Grid & Patch Mathematics
* **Detail Resolution**: Defines the total detail placement grid across the terrain. Higher values yield finer placement precision.
* **Detail Resolution Per Patch**: Acts as a **divisor** that groups grid cells into rendered patches.
  \\[\text{Patches Per Axis} = \frac{\text{Detail Resolution}}{\text{Detail Resolution Per Patch}}\\]
  Higher patch divisor values reduce draw calls and CPU overhead, but occlusion culling evaluates entire patches at once—meaning off-screen foliage within an active patch remains in the render pipeline.

### 3.2 Scatter Modes
* **Instance Count Mode**: Allows manual brush opacity/strength controls for specific detail placement. Overall density scales globally via **Detail Density Scale**.
* **Coverage Mode**: Procedurally distributes detail instances based on individual detail density parameters; instance locations are generated randomly.

### 3.3 Dual-Prefab Grass Performance Strategy
To maintain high visual grass density without GPU bottlenecks:
1. Create a primary shadow-casting grass prefab for key hero areas.
2. Duplicate the prefab (`Ctrl + D`) and **disable `Cast Shadows`**.
3. Set the non-shadow prefab's height scale low (`0.1` to `1.0`), assign a lower-polygon mesh, and increase detail density to fill ground gaps cheaply.
4. Match grass color tint to the underlying terrain texture to allow lower density settings without revealing bare ground.

### 3.4 Tree & Detail LOD Fixes
* **Fixing Scaling/Rotation Locks**: Standard detail meshes without LOD components lose rotation and scaling functionality in Unity Terrain.
* **LOD Setup SOP**:
  1. Unpack the source model prefab.
  2. Add a **LOD Group** component.
  3. Assign the desired mesh to **LOD0** and remove extra LOD slots.
  4. Save as a new clean prefab and assign it to the Terrain Tree/Detail list.
* **Mitigating Dark Tree Shadows**: In URP/HDRP, trees lack real-time GI support and generate harsh black shadows. Create low-intensity **Directional Bounce Lights** as child objects under the main Directional Light to soften tree shadows.

---

## 4. WET TERRAIN, PUDDLES & DECAL FILTERING

### 4.1 Wet Mask Map Specification
Create a dedicated puddle texture map with:
* **Red Channel (Metallic)** = `0` (Black).
* **Alpha Channel (Smoothness)** = `1` (White).

### 4.2 Localized Puddles vs. Decal Layer Filtering
* **Local Puddle Layers**: Paint a dedicated terrain layer using the Wet Mask Map; adjust the color tint to control puddle depth and reflectivity. Integrate with Reflection Probes or Screen Space Reflections (SSR).
* **Global Wetness via HDRP Decal Projectors**: Project an HDRP Decal using the Wet Mask over the environment.
* **Preventing Indoor Moisture Leaks**:
  1. Open **Project Settings > HDRP Settings** and enable **Decal Layers**.
  2. Assign outdoor surfaces (roofs, terrain) to the target Decal Layer.
  3. Exclude interior meshes from the Decal Layer so building interiors remain dry.

---

## 5. ATMOSPHERIC LIGHTING, CLOUD SHADOWS & VOLUMES

### 5.1 Animated Procedural Cloud Shadow Cookies
Simulate moving cloud shadows without rendering 3D clouds:
1. Generate two high-contrast, seamless noise textures in an image editor (white = light, dark = shadow).
2. Build a custom render texture shader that animates UV movement across both textures using `Time * Speed` vectors in opposite directions.
3. Create a **Custom Render Texture** asset using this shader, set color format to `sRGB`, wrap mode to `Repeat`, and update mode to `Realtime`.
4. Assign the texture asset to the Directional Light's **Cookie** slot (set size to ~`1500x1500`).
5. Combine with HDRP **Volumetric Fog** to automatically generate dynamic atmospheric God Rays.

### 5.2 Post-Processing Volume Hierarchies
* **Global Volumes**: Apply baseline atmospheric overrides across the entire scene.
* **Local Box Volumes**: Place local Box Volumes with **Box Colliders** inside distinct zones (e.g., caves, interiors).
* **Priority & Blend Distance**:
  * Set **Priority** higher than the Global Volume so local overrides take effect when the camera enters the collider.
  * Tune **Blend Distance** to control transition smoothing when crossing boundaries.

---

## 6. ADVANCED SHADER GRAPH TERRAIN SHADING (UNITY 6.3+ / URP)

### 6.1 Terrain Graph Setup
1. Create a shader via **Create > Shader Graph > URP > Terrain Lit**.
2. Use the **Terrain Texture** node inside subgraphs to sample terrain layer inputs (Index, Normal Scale, Color Tint) directly.

### 6.2 Advanced Shader Techniques
* **Hexagon Tiling**: Replaces standard square UV tiling with hexagonal sampling to eliminate visible repetition patterns across large terrains.
* **Distance Fading**: Blends out hard transition lines between detailed foreground layers and low-cost background layers, allowing transition boundaries to be moved closer to the camera to optimize rendering.
* **CHNOS Array Dither**: Packs terrain textures into Texture Arrays and uses dither blending; processes 4 terrain layers in just 6 texture samples, drastically lowering draw costs for XR/Mobile platforms.
* **Parallax Occlusion Mapping (POM)**: Implements ray-marched height offsets in Shader Graph to achieve physical surface depth without geometry or tessellation costs.

---

## 7. TROUBLESHOOTING & COMMON PITFALLS MATRIX

| Issue / Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| Pink / Broken Terrain Material | Missing Diffusion Profile in HDRP material. | Open material inspector, locate **Diffusion Profile**, and select the project profile asset. |
| Detail / Tree Scale & Rotation Locked | Prefab lacks Unity `LOD Group` structure. | Unpack prefab, add `LOD Group`, assign mesh to `LOD0`, save new prefab, and re-assign to terrain. |
| Sculpted Holes Vanish in Standalone Build | **Terrain Hole** option disabled in build settings. | Enable **Terrain Hole** under **Project Settings**. |
| Harsh Black Shadows on Trees | URP/HDRP trees lack real-time GI support. | Add low-intensity **Directional Bounce Lights** as child objects under main Light. |
| Decal Moisture Leaking Indoors | Decal Projector affecting all scene layers indiscriminately. | Enable **Decal Layers** in HDRP Project Settings; assign outdoor objects while excluding interior meshes. |
| Low Performance with Dense Foliage | Hero grass prefabs casting dynamic shadows across large areas. | Duplicate grass prefab, **disable Cast Shadows**, lower height range (`0.1-1.0`), and use as gap-filler. |
```

---

You can copy and paste the Markdown block directly into your source notes or AI knowledge base. Let me know if you would like any further adjustments or technical expansions!