from pathlib import Path

root = Path("MiYouTube-src")

main_fragment = root / "app/src/main/java/org/schabi/newpipe/fragments/MainFragment.java"
s = main_fragment.read_text(encoding="utf-8")
for unused in [
    "import static com.google.android.material.tabs.TabLayout.INDICATOR_GRAVITY_BOTTOM;\n",
    "import androidx.annotation.ColorInt;\n",
    "import org.schabi.newpipe.util.ThemeHelper;\n",
]:
    s = s.replace(unused, "")

s = s.replace(
    'NavigationHelper.openSearchFragment(getFM(), ServiceHelper.getSelectedServiceId(activity), "");',
    'NavigationHelper.openSearchFragment(\n'
    '                    getFM(), ServiceHelper.getSelectedServiceId(activity), "");',
)
s = s.replace(
    'tabLayout.setTabRippleColor(ColorStateList.valueOf(Color.rgb(255, 0, 51)).withAlpha(32));',
    'tabLayout.setTabRippleColor(\n'
    '                ColorStateList.valueOf(Color.rgb(255, 0, 51)).withAlpha(32));',
)
main_fragment.write_text(s, encoding="utf-8")

main_activity = root / "app/src/main/java/org/schabi/newpipe/MainActivity.java"
s = main_activity.read_text(encoding="utf-8")
s = s.replace("import org.schabi.newpipe.util.KioskTranslator;\n", "")
main_activity.write_text(s, encoding="utf-8")

print("Checkstyle 1.3.0 corregido")
