# Design System Specification: Architectural Integrity & The Ethical Lens

## 1. Overview & Creative North Star: "The Architectural Curator"
This design system rejects the "template" aesthetic of the modern web in favor of **Architectural Integrity**. We are building a space for FairHire AI that feels like a high-end editorial publication merged with a sophisticated architectural firm.

**Creative North Star: The Architectural Curator**
Our goal is to convey "Trust" not through heavy borders and blue boxes, but through **intentional whitespace, tonal depth, and typographic authority.** We move beyond the flat grid by using "Negative Space as Structure." By utilizing asymmetric layouts—where a headline might sit off-center against a deep navy field—we create a sense of bespoke craftsmanship. The interface shouldn't feel like a software tool; it should feel like a premium consultation environment.

---

## 2. Colors: Tonal Depth & The Teal Spark
We utilize a monochromatic base of Deep Navy and Slate Blue to establish a "Trust Anchor," punctuated by a vibrant Teal accent that represents AI-driven insight.

### The Palette
*   **Primary (Deep Navy):** `#0B1F3A` (as `primary_container`). This is our foundation. It represents the "Architectural Base."
*   **Secondary (Slate Blue):** `#4a607c`. Used for supportive elements and secondary hierarchy.
*   **Tertiary (Vibrant Teal):** `#14B8A6` (mapped to `tertiary_fixed`). This is the "Spark of Intelligence"—use it sparingly for high-value actions and data highlights.
*   **Surface:** `#f9f9ff`. A crisp, gallery-white that provides the "Breathing Room."

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to define sections. We define boundaries through **Background Color Shifts**. 
*   To separate a sidebar from a main feed, transition from `surface` to `surface_container_low`. 
*   If a visual break is required, use a 48px vertical gap—never a line.

### Surface Hierarchy & Nesting
Treat the UI as a series of stacked, premium materials.
1.  **Base Layer:** `surface` (The gallery floor)
2.  **Section Layer:** `surface_container_low` (The raised platform)
3.  **Content Card:** `surface_container_lowest` (The white paper sitting on the platform)
4.  **Interaction Layer:** `surface_bright` (The illuminated focal point)

### Signature Textures & Glass
To avoid a "flat" feel, use a subtle **Linear Gradient** for hero sections: `primary_container` (100%) to `primary` (100%) at a 135-degree angle. For floating navigation or modals, apply **Glassmorphism**: `surface_container_low` at 80% opacity with a `24px` backdrop blur.

---

## 3. Typography: Editorial Authority
We pair the geometric precision of **Manrope** with the functional clarity of **Inter**.

*   **Display (Manrope):** These are your "Editorial Statements." Use `display-lg` (3.5rem) with tightened letter-spacing (-0.02em) to create an authoritative, architectural presence.
*   **Headlines (Manrope):** Use `headline-md` (1.75rem) for section titles. Ensure they have generous leading (1.4) to allow the "air" of the system to flow.
*   **Body (Inter):** All functional text uses Inter. `body-lg` (1rem) is the standard for readability. 
*   **Labels (Inter):** `label-md` (0.75rem) should always be in **All Caps** with `0.05em` letter-spacing when used for category tags or small metadata to maintain the "Architectural" feel.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are too "software-generic." We use **Ambient Light** and **Material Stacking**.

*   **The Layering Principle:** Instead of a shadow, place a `surface_container_lowest` card atop a `surface_container` background. The subtle 2% shift in value creates a "Soft Lift."
*   **Ambient Shadows:** For elevated elements (e.g., Modals), use a multi-layered shadow: 
    *   `0px 4px 20px rgba(7, 28, 54, 0.04)`
    *   `0px 12px 40px rgba(7, 28, 54, 0.08)`
    *   *Shadow color must be a tint of the `on_surface` (Deep Navy), never pure black.*
*   **The "Ghost Border" Fallback:** If a container must be defined on a complex background, use the `outline_variant` token at **15% opacity**. It should be felt, not seen.

---

## 5. Components: Precision & Minimalist Form

### Buttons: The "Statement" Component
*   **Primary:** Solid `primary_container` with `on_primary` text. No border. Radius: `md` (0.375rem).
*   **Secondary:** Ghost style. No background, `outline_variant` at 20% for the border.
*   **Accent (Teal):** Used *only* for the final conversion point (e.g., "Submit Hire"). Uses `tertiary_fixed` with `on_tertiary_fixed`.

### Input Fields: The "Architectural Line"
*   **Styling:** Background of `surface_container_low`. A single 2px bottom-border of `outline_variant` instead of a full box. Upon focus, the bottom border transitions to `tertiary` (Teal).
*   **Labels:** Floating labels using `label-md` in `secondary`.

### Cards & Lists: The "Whitespace" Rule
*   **Cards:** Use `surface_container_lowest`. Forbid dividers. 
*   **Lists:** List items are separated by `16px` of vertical whitespace. On hover, the background shifts to `surface_container_high` with a `4px` Teal vertical accent line on the far left.

### AI Insight Chips
*   Specialized components for FairHire AI. Use a Glassmorphic teal background: `rgba(20, 184, 166, 0.1)` with a `1px` teal border at 20% opacity. This makes AI suggestions feel "Luminous."

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical margins. A 2/3 vs 1/3 split for content creates a high-end editorial look.
*   **Do** use "Teal Highlights." Only use the Teal accent for elements that involve AI calculation or critical calls to action.
*   **Do** stack surfaces (Lowest → Low → High) to guide the user's eye toward the most important data.

### Don't:
*   **Don't** use 100% black. Use Deep Navy (`#0B1F3A`) for all "dark" elements to maintain tonal richness.
*   **Don't** use standard "Drop Shadows." If it looks like a default Material Design shadow, it's too heavy.
*   **Don't** use dividers. Use the Spacing Scale (Vertical space) to separate thoughts and sections.
*   **Don't** crowd the interface. If you aren't sure, add `24px` more padding. Luxury is defined by the space you *don't* use.