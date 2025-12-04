# 🚀 QUICK START GUIDE

## What You Need to Do RIGHT NOW on Your Computer

### ✅ STEP 1: Update Your Data (5 minutes)

1. Open `data.csv` in Excel or a text editor
2. Replace `Topic_1`, `Topic_2`, etc. with your actual topic names
3. Update any numbers if needed
4. Save the file

**Example:**
```
# Change this:
Topic_1,Kyocera,27,112,3,4100

# To this:
Sustainability,Kyocera,27,112,3,4100
```

---

### ✅ STEP 2: Generate Visualizations (2 minutes)

Open your terminal/command prompt in this folder and run:

```bash
python visualizations.py
```

This creates 6 HTML files in the `output/` folder.

---

### ✅ STEP 3: Choose Your Presentation Method

Pick ONE of these three options:

## 🏆 **OPTION A: Static Images (EASIEST)**

**Best for:** Any PowerPoint version, guaranteed to work

**Steps:**
1. Open each HTML file in your browser (double-click it)
2. Take a screenshot (Win+Shift+S or Cmd+Shift+4)
3. Paste into PowerPoint
4. Done!

**Result:** Professional images, no code needed on presentation computer ✅

---

## 🎯 **OPTION B: Interactive Single Dashboard (RECOMMENDED)**

**Best for:** Impressive presentations, works offline

**Steps:**
1. Run this command:
   ```bash
   python create_presentation_dashboard.py
   ```

2. This creates `output/presentation_dashboard.html`

3. **Option B1 - Present from browser:**
   - Open the HTML file in your browser
   - Press F11 for fullscreen
   - Present directly! (Use tabs to switch between visualizations)
   - Copy this file to presentation computer - works offline!

4. **Option B2 - Link from PowerPoint:**
   - In PowerPoint: Insert → Link → select the HTML file
   - During presentation, click link to open interactive dashboard
   - Press F11 for fullscreen in browser

**Result:** Fully interactive, all 6 charts with tabs, portable ✅

---

## 🖼️ **OPTION C: High-Quality PNG Images**

**Best for:** Print or high-resolution needs

**Requirements:** Chrome browser installed

**Steps:**
1. Install Chrome if not already installed
2. Run this command:
   ```bash
   pip install kaleido
   python generate_static_images.py
   ```

3. Find PNG files in `output/png/` folder

4. In PowerPoint: Insert → Pictures → select PNG files

**Result:** High-quality static images ✅

---

## 📋 SUMMARY TABLE

| Method | Interactive? | Works Offline? | PowerPoint? | Difficulty |
|--------|--------------|----------------|-------------|------------|
| **Option A: Screenshots** | ❌ | ✅ | ✅ | ⭐ Easy |
| **Option B: Dashboard** | ✅ | ✅ | ✅ (linked) | ⭐⭐ Medium |
| **Option C: PNG Export** | ❌ | ✅ | ✅ | ⭐⭐ Medium |

---

## 🎬 FOR YOUR PRESENTATION COMPUTER

### If using Option A (Screenshots):
- **Take:** Your PowerPoint file
- **That's it!** Everything is embedded

### If using Option B (Dashboard):
- **Take:**
  - Your PowerPoint file (if linking)
  - `output/presentation_dashboard.html` file
- **Or just:** Open `presentation_dashboard.html` directly in browser (F11 fullscreen)

### If using Option C (PNG):
- **Take:** Your PowerPoint file
- **That's it!** PNG images are embedded

---

## 💡 RECOMMENDED WORKFLOW

**For beginners:**
→ Use **Option A** (Screenshots) - Always works!

**For impressive presentations:**
→ Use **Option B** (Dashboard) - Copy HTML file to presentation laptop, open in browser

**For printed materials:**
→ Use **Option C** (PNG export) - High resolution images

---

## ⚡ QUICK REFERENCE COMMANDS

```bash
# Generate all HTML visualizations
python visualizations.py

# Generate interactive dashboard (ALL IN ONE FILE)
python create_presentation_dashboard.py

# Generate PNG images (requires Chrome)
python generate_static_images.py
```

---

## ❓ TROUBLESHOOTING

**Q: Python not found**
- Install Python from python.org

**Q: Missing packages error**
- Run: `pip install plotly pandas numpy`

**Q: PNG generation fails**
- You need Chrome browser installed
- Or just use Option A or B instead!

**Q: HTML file doesn't open in PowerPoint**
- Don't embed it, just link to it
- Or use screenshot method (Option A)

---

## 📞 NEED HELP?

Refer to `VISUALIZATION_GUIDE.md` for detailed documentation.
