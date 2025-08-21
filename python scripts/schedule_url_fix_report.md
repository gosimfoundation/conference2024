# Schedule URL Fix Report

## Summary
Successfully fixed escaped backslash URLs in all HTML files within the `schedules/` and `zh/schedules/` folders.

## Problem
The speaker links and other relative URLs in the schedule HTML files had escaped backslashes that prevented proper navigation. For example:
- `href="\.\./speakers/gao\-shan\.html"` (broken)
- `href="\.\./index\.html"` (broken)

## Solution
Created and executed a Python script (`fix_schedule_urls.py`) that:

1. **Fixed speaker URLs**: `\.\./speakers/name\.html` → `../speakers/name.html`
2. **Fixed relative URLs**: `\.\./path\.html` → `../path.html`
3. **Fixed double escaped URLs**: `\.\./\.\./path\.html` → `../../path.html`
4. **Fixed escaped hyphens**: `name\-surname\.html` → `name-surname.html`
5. **Fixed remaining escaped characters**: `\.` → `.` and `\/` → `/`

## Results
- **Total files processed**: 276 HTML files
- **Files with fixes applied**: 276 files (100%)
- **Folders processed**:
  - `schedules/` (138 files)
  - `zh/schedules/` (138 files)

## Example Fix
**Before:**
```html
<a href="\.\./speakers/gao\-shan\.html" class="link-block-3 w-inline-block">
```

**After:**
```html
<a href="../speakers/gao-shan.html" class="link-block-3 w-inline-block">
```

## Verification
- ✅ No remaining escaped backslash URLs found in `schedules/*.html`
- ✅ No remaining escaped backslash URLs found in `zh/schedules/*.html`
- ✅ All speaker links now properly navigate to the speakers directory
- ✅ All relative navigation links now work correctly

## Files Created
- `fix_schedule_urls.py` - The script used to fix the URLs
- `schedule_url_fix_report.md` - This report

The speaker links in all schedule pages should now work correctly and navigate to the appropriate speaker profile pages.
