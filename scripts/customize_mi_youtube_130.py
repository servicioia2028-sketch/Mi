from pathlib import Path
import re
root = Path('MiYouTube-src')

p=root/'app/build.gradle.kts'; s=p.read_text()
s=re.sub(r'versionCode\s*=\s*System\.getProperty\("versionCodeOverride"\)\?\.toInt\(\) \?: \d+', 'versionCode = System.getProperty("versionCodeOverride")?.toInt() ?: 1300', s)
s=re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.3.0"', s, count=1)
p.write_text(s)

p=root/'app/src/main/res/values/colors.xml'; s=p.read_text()
for a,b in {'#222222':'#0F0F0F','#424242':'#171717','#ff5252':'#FF0033','#313131':'#171717','#474747':'#242424','#23454545':'#1A1A1A','#202020':'#1D1D1D','#96717171':'#33FF0033'}.items(): s=s.replace(a,b)
p.write_text(s)
p=root/'app/src/main/res/values/colors_services.xml'; s=p.read_text().replace('#e53935','#0F0F0F').replace('#992722','#0F0F0F'); p.write_text(s)

brand='''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
<path android:fillColor="#101010" android:pathData="M12,8 L96,8 L104,16 L104,92 L96,100 L12,100 L4,92 L4,16 Z"/>
<path android:fillColor="#FF0033" android:pathData="M20,28 L54,48 L88,28 L78,65 L54,79 L30,65 Z"/>
<path android:fillColor="#B7B7B7" android:pathData="M20,28 L30,65 L54,79 L54,48 Z"/>
<path android:fillColor="#E2E2E2" android:pathData="M88,28 L78,65 L54,79 L54,48 Z"/>
<path android:fillColor="#0F0F0F" android:pathData="M39,43 L69,43 L69,70 L39,70 Z"/>
<path android:fillColor="#FFFFFF" android:pathData="M48,47 L48,67 L65,57 Z"/>
</vector>'''
res=root/'app/src/main/res'
(res/'drawable/ic_miyoutube_brand.xml').write_text(brand)
(res/'drawable/premium_card.xml').write_text('''<selector xmlns:android="http://schemas.android.com/apk/res/android"><item android:state_pressed="true"><shape><solid android:color="#252525"/><corners android:radius="16dp"/><stroke android:width="1dp" android:color="#333333"/></shape></item><item><shape><solid android:color="#171717"/><corners android:radius="16dp"/><stroke android:width="1dp" android:color="#242424"/></shape></item></selector>''')
(res/'drawable/premium_search_bar.xml').write_text('''<selector xmlns:android="http://schemas.android.com/apk/res/android"><item android:state_pressed="true"><shape><solid android:color="#303030"/><corners android:radius="28dp"/></shape></item><item><shape><solid android:color="#232323"/><corners android:radius="28dp"/><stroke android:width="1dp" android:color="#333333"/></shape></item></selector>''')
(res/'drawable/premium_thumbnail.xml').write_text('''<shape xmlns:android="http://schemas.android.com/apk/res/android"><solid android:color="#252525"/><corners android:radius="12dp"/></shape>''')
(res/'drawable/premium_duration.xml').write_text('''<shape xmlns:android="http://schemas.android.com/apk/res/android"><solid android:color="#D9000000"/><corners android:radius="5dp"/></shape>''')
(res/'drawable/premium_drawer_bg.xml').write_text('''<shape xmlns:android="http://schemas.android.com/apk/res/android"><solid android:color="#0F0F0F"/><corners android:topRightRadius="24dp" android:bottomRightRadius="24dp"/></shape>''')

mip=res/'mipmap-anydpi'; mip.mkdir(parents=True,exist_ok=True); (mip/'ic_launcher.xml').write_text(brand)
for d in ['mipmap-mdpi','mipmap-hdpi','mipmap-xhdpi','mipmap-xxhdpi','mipmap-xxxhdpi']:
    for name in ['ic_launcher.png','ic_launcher_foreground.png']:
        q=res/d/name
        if q.exists(): q.unlink()
(res/'mipmap-anydpi-v26/ic_launcher.xml').write_text('''<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/black_background_color"/><foreground android:drawable="@drawable/ic_miyoutube_brand"/><monochrome android:drawable="@drawable/ic_miyoutube_brand"/></adaptive-icon>''')
for rel in ['drawable/splash_background.xml','drawable-night/splash_background.xml','drawable-v23/splash_background.xml','drawable-night-v23/splash_background.xml']:
    (res/rel).write_text('''<?xml version="1.0" encoding="utf-8"?><layer-list xmlns:android="http://schemas.android.com/apk/res/android"><item android:drawable="@color/black_background_color"/><item android:width="108dp" android:height="108dp" android:gravity="center" android:drawable="@drawable/ic_miyoutube_brand"/></layer-list>''')

(res/'layout/fragment_main.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" android:layout_width="match_parent" android:layout_height="match_parent" android:background="#0F0F0F">
<LinearLayout android:id="@+id/premium_home_header" android:layout_width="match_parent" android:layout_height="72dp" android:layout_alignParentTop="true" android:gravity="center_vertical" android:orientation="horizontal" android:paddingStart="12dp" android:paddingEnd="12dp">
<TextView android:id="@+id/premium_search_button" android:layout_width="match_parent" android:layout_height="48dp" android:background="@drawable/premium_search_bar" android:drawableStart="@drawable/ic_search" android:drawablePadding="10dp" android:gravity="center_vertical" android:paddingStart="18dp" android:paddingEnd="18dp" android:text="Buscar videos, canales y más" android:textColor="#BDBDBD" android:textSize="15sp"/>
</LinearLayout>
<org.schabi.newpipe.views.ScrollableTabLayout android:id="@+id/main_tab_layout" android:layout_width="match_parent" android:layout_height="64dp" android:layout_alignParentBottom="true" android:background="#0F0F0F" app:tabGravity="fill" app:tabIndicatorColor="#FF0033" app:tabIndicatorGravity="top" app:tabIndicatorHeight="2dp" app:tabMinWidth="64dp" app:tabMode="fixed" app:tabRippleColor="#22FF0033" app:tabTextColor="#9E9E9E" app:tabSelectedTextColor="#FF0033"/>
<androidx.viewpager.widget.ViewPager android:id="@+id/pager" android:layout_width="match_parent" android:layout_height="match_parent" android:layout_below="@id/premium_home_header" android:layout_above="@id/main_tab_layout"/>
</RelativeLayout>''')

(res/'layout/list_stream_item.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:id="@+id/itemRoot" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginStart="10dp" android:layout_marginEnd="10dp" android:layout_marginTop="5dp" android:layout_marginBottom="5dp" android:background="@drawable/premium_card" android:clickable="true" android:focusable="true" android:padding="8dp">
<ImageView android:id="@+id/itemThumbnailView" android:layout_width="142dp" android:layout_height="80dp" android:background="@drawable/premium_thumbnail" android:clipToOutline="true" android:scaleType="centerCrop" android:src="@drawable/placeholder_thumbnail_video" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent"/>
<org.schabi.newpipe.views.NewPipeTextView android:id="@+id/itemDurationView" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginEnd="5dp" android:layout_marginBottom="5dp" android:background="@drawable/premium_duration" android:paddingHorizontal="5dp" android:paddingVertical="2dp" android:textColor="#FFFFFF" android:textSize="10sp" app:layout_constraintBottom_toBottomOf="@id/itemThumbnailView" app:layout_constraintEnd_toEndOf="@id/itemThumbnailView" tools:text="12:34"/>
<org.schabi.newpipe.views.NewPipeTextView android:id="@+id/itemVideoTitleView" android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="10dp" android:ellipsize="end" android:maxLines="2" android:textColor="#FFFFFF" android:textSize="16sp" android:textStyle="bold" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toEndOf="@id/itemThumbnailView" app:layout_constraintTop_toTopOf="@id/itemThumbnailView" tools:text="Título del video"/>
<org.schabi.newpipe.views.NewPipeTextView android:id="@+id/itemUploaderView" android:layout_width="0dp" android:layout_height="wrap_content" android:ellipsize="end" android:lines="1" android:textColor="#BDBDBD" android:textSize="13sp" app:layout_constraintEnd_toEndOf="@id/itemVideoTitleView" app:layout_constraintStart_toStartOf="@id/itemVideoTitleView" app:layout_constraintTop_toBottomOf="@id/itemVideoTitleView" tools:text="Canal"/>
<org.schabi.newpipe.views.NewPipeTextView android:id="@+id/itemAdditionalDetails" android:layout_width="0dp" android:layout_height="wrap_content" android:ellipsize="end" android:lines="1" android:textColor="#9E9E9E" android:textSize="12sp" app:layout_constraintBottom_toBottomOf="@id/itemThumbnailView" app:layout_constraintEnd_toEndOf="@id/itemVideoTitleView" app:layout_constraintStart_toStartOf="@id/itemVideoTitleView" tools:text="620 K vistas • hace 3 días"/>
<org.schabi.newpipe.views.AnimatedProgressBar android:id="@+id/itemProgressView" style="@style/Widget.AppCompat.ProgressBar.Horizontal" android:layout_width="0dp" android:layout_height="3dp" android:progressDrawable="?progress_horizontal_drawable" app:layout_constraintBottom_toBottomOf="@id/itemThumbnailView" app:layout_constraintEnd_toEndOf="@id/itemThumbnailView" app:layout_constraintStart_toStartOf="@id/itemThumbnailView"/>
</androidx.constraintlayout.widget.ConstraintLayout>''')

p=res/'layout/toolbar_search_layout.xml'; s=p.read_text()
s=s.replace('android:background="@null"','android:background="@drawable/premium_search_bar"').replace('android:layout_marginTop="4dp"','android:layout_marginTop="6dp"').replace('android:layout_marginBottom="4dp"','android:layout_marginBottom="6dp"').replace('android:layout_marginRight="48dp"','android:layout_marginLeft="8dp"\n        android:layout_marginRight="52dp"\n        android:paddingLeft="16dp"\n        android:paddingRight="16dp"')
p.write_text(s)

(res/'layout/toolbar_layout.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical">
<androidx.appcompat.widget.Toolbar android:id="@+id/toolbar" android:layout_width="match_parent" android:layout_height="60dp" android:background="#0F0F0F" android:gravity="center_vertical" android:minHeight="60dp" android:theme="@style/ToolbarTheme">
<ImageView android:layout_width="32dp" android:layout_height="32dp" android:layout_marginEnd="8dp" android:src="@drawable/ic_miyoutube_brand" tools:ignore="ContentDescription"/>
<include android:id="@+id/toolbar_search_container" layout="@layout/toolbar_search_layout" android:visibility="gone" tools:visibility="visible"/>
</androidx.appcompat.widget.Toolbar>
</LinearLayout>''')
p=res/'layout/activity_main.xml'; s=p.read_text().replace('android:layout_marginTop="?attr/actionBarSize"','android:layout_marginTop="60dp"'); p.write_text(s)

(res/'layout/drawer_layout.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<com.google.android.material.navigation.NavigationView xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" android:id="@+id/navigation" android:layout_width="304dp" android:layout_height="match_parent" android:layout_gravity="start" android:background="@drawable/premium_drawer_bg" android:orientation="vertical" app:headerLayout="@layout/drawer_header" app:itemIconTint="#BDBDBD" app:itemTextColor="#FFFFFF"/>
''')
(res/'layout/drawer_header.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools" android:layout_width="match_parent" android:layout_height="142dp" android:background="#0F0F0F" android:paddingTop="18dp">
<ImageView android:id="@+id/brand_icon" android:layout_width="52dp" android:layout_height="52dp" android:layout_marginStart="18dp" android:src="@drawable/ic_miyoutube_brand" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent" tools:ignore="ContentDescription"/>
<org.schabi.newpipe.views.NewPipeTextView android:id="@+id/drawer_header_newpipe_title" android:layout_width="0dp" android:layout_height="52dp" android:layout_marginStart="12dp" android:layout_marginEnd="18dp" android:gravity="center_vertical" android:maxLines="1" android:text="@string/app_name" android:textColor="#FFFFFF" android:textSize="25sp" android:textStyle="bold" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toEndOf="@id/brand_icon" app:layout_constraintTop_toTopOf="@id/brand_icon"/>
<LinearLayout android:id="@+id/service_row" android:layout_width="0dp" android:layout_height="44dp" android:layout_marginStart="18dp" android:layout_marginEnd="18dp" android:layout_marginTop="12dp" android:background="@drawable/premium_search_bar" android:gravity="center_vertical" android:orientation="horizontal" android:paddingStart="12dp" android:paddingEnd="8dp" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toBottomOf="@id/brand_icon">
<ImageView android:id="@+id/drawer_header_service_icon" android:layout_width="20dp" android:layout_height="20dp" app:tint="#FF0033" tools:ignore="ContentDescription" tools:src="@drawable/ic_smart_display"/>
<org.schabi.newpipe.views.NewPipeTextView android:id="@+id/drawer_header_service_view" android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="10dp" android:layout_weight="1" android:ellipsize="end" android:maxLines="1" android:textColor="#FFFFFF" android:textSize="14sp" android:textStyle="bold" tools:text="YouTube"/>
<ImageView android:id="@+id/drawer_arrow" android:layout_width="24dp" android:layout_height="24dp" android:src="@drawable/ic_arrow_drop_down" app:tint="#BDBDBD" tools:ignore="ContentDescription"/>
</LinearLayout>
<Button android:id="@+id/drawer_header_action_button" android:layout_width="match_parent" android:layout_height="0dp" android:background="?selectableItemBackground" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintTop_toTopOf="parent"/>
</androidx.constraintlayout.widget.ConstraintLayout>''')

p=root/'app/src/main/java/org/schabi/newpipe/fragments/MainFragment.java'; s=p.read_text()
s=s.replace('mainTabsPositionBottom = prefs.getBoolean(mainTabsPositionKey, false);','mainTabsPositionBottom = true;').replace('final boolean newMainTabsPosition = prefs.getBoolean(mainTabsPositionKey, false);','final boolean newMainTabsPosition = true;')
s=s.replace('tabToSet.setIcon(tab.getTabIconRes(requireContext()));\n                tabToSet.setContentDescription(tab.getTabName(requireContext()));','tabToSet.setIcon(tab.getTabIconRes(requireContext()));\n                tabToSet.setText(tab.getTabName(requireContext()));\n                tabToSet.setContentDescription(tab.getTabName(requireContext()));')
s=s.replace('setTitle(tabsList.get(tabPosition).getTabName(requireContext()));','setTitle(R.string.app_name);')
needle='''        binding.mainTabLayout.addOnTabSelectedListener(this);\n\n        setupTabs();'''
replacement='''        binding.mainTabLayout.addOnTabSelectedListener(this);\n        binding.premiumSearchButton.setOnClickListener(v -> {\n            try {\n                NavigationHelper.openSearchFragment(getFM(), ServiceHelper.getSelectedServiceId(activity), "");\n            } catch (final Exception e) {\n                ErrorUtil.showUiErrorSnackbar(this, "Opening search fragment", e);\n            }\n        });\n\n        setupTabs();'''
s=s.replace(needle,replacement)
start=s.index('    private void updateTabLayoutPosition() {'); end=s.index('\n    @Override\n    public void onTabSelected', start)
method='''    private void updateTabLayoutPosition() {\n        final ScrollableTabLayout tabLayout = binding.mainTabLayout;\n        final ViewPager viewPager = binding.pager;\n        final var tabParams = (RelativeLayout.LayoutParams) tabLayout.getLayoutParams();\n        final var pagerParams = (RelativeLayout.LayoutParams) viewPager.getLayoutParams();\n        tabParams.removeRule(ALIGN_PARENT_TOP);\n        tabParams.addRule(ALIGN_PARENT_BOTTOM);\n        pagerParams.removeRule(BELOW);\n        pagerParams.removeRule(ABOVE);\n        pagerParams.addRule(BELOW, R.id.premium_home_header);\n        pagerParams.addRule(ABOVE, R.id.main_tab_layout);\n        tabLayout.setSelectedTabIndicatorGravity(INDICATOR_GRAVITY_TOP);\n        tabLayout.setLayoutParams(tabParams);\n        viewPager.setLayoutParams(pagerParams);\n        tabLayout.setBackgroundColor(Color.rgb(15, 15, 15));\n        final int[][] states = new int[][] {new int[] {android.R.attr.state_selected}, new int[] {}};\n        final int[] colors = new int[] {Color.rgb(255, 0, 51), Color.rgb(158, 158, 158)};\n        final ColorStateList navColors = new ColorStateList(states, colors);\n        tabLayout.setTabRippleColor(ColorStateList.valueOf(Color.rgb(255, 0, 51)).withAlpha(32));\n        tabLayout.setTabIconTint(navColors);\n        tabLayout.setTabTextColors(navColors);\n        tabLayout.setSelectedTabIndicatorColor(Color.rgb(255, 0, 51));\n    }\n'''
s=s[:start]+method+s[end:]; p.write_text(s)

p=root/'app/src/main/java/org/schabi/newpipe/MainActivity.java'; s=p.read_text()
s=re.sub(r'\n\s*//Kiosks\n.*?\n\s*//Settings and About', '\n\n        // Menú secundario simplificado para una interfaz más limpia.\n        // Settings and About', s, flags=re.S)
s=re.sub(r'\n\s*drawerLayoutBinding\.navigation\.getMenu\(\)\n\s*\.add\(R\.id\.menu_options_about_group, ITEM_ID_DONATION, ORDER,\n\s*R\.string\.donation_title\)\n\s*\.setIcon\(R\.drawable\.volunteer_activism_ic\);', '', s)
p.write_text(s)

(root/'MI-YOUTUBE-NOTICE.txt').write_text('''Mi YouTube 1.3.0\nBasado en TeamNewPipe/NewPipe v0.29.0 y NewPipeExtractor.\nLicencia GPL-3.0-or-later.\nInterfaz personalizada premium oscura con navegación inferior, búsqueda, tarjetas redondeadas, nuevo branding e icono.\nNo es una aplicación oficial de YouTube ni de NewPipe.\n''')
print('Mi YouTube 1.3.0 personalizado')
