from pathlib import Path
import runpy
import re

# Reutiliza el rediseño 1.3.0 ya probado y añade la capa Universal.
runpy.run_path('scripts/customize_mi_youtube_130.py', run_name='__main__')

root = Path('MiYouTube-src')
res = root / 'app/src/main/res'

# Versión Universal 1.3.1
p = root / 'app/build.gradle.kts'
s = p.read_text(encoding='utf-8')
s = re.sub(
    r'versionCode\s*=\s*System\.getProperty\("versionCodeOverride"\)\?\.toInt\(\) \?: \d+',
    'versionCode = System.getProperty("versionCodeOverride")?.toInt() ?: 1310',
    s,
)
s = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.3.1"', s, count=1)
p.write_text(s, encoding='utf-8')

# Estados de foco visibles para control remoto / D-pad.
(res / 'drawable/premium_card.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_focused="true">
        <shape>
            <solid android:color="#252525"/>
            <corners android:radius="16dp"/>
            <stroke android:width="3dp" android:color="#FF0033"/>
        </shape>
    </item>
    <item android:state_pressed="true">
        <shape>
            <solid android:color="#303030"/>
            <corners android:radius="16dp"/>
            <stroke android:width="2dp" android:color="#FF335C"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="#171717"/>
            <corners android:radius="16dp"/>
            <stroke android:width="1dp" android:color="#242424"/>
        </shape>
    </item>
</selector>''', encoding='utf-8')

(res / 'drawable/premium_search_bar.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_focused="true">
        <shape>
            <solid android:color="#292929"/>
            <corners android:radius="28dp"/>
            <stroke android:width="3dp" android:color="#FF0033"/>
        </shape>
    </item>
    <item android:state_pressed="true">
        <shape>
            <solid android:color="#303030"/>
            <corners android:radius="28dp"/>
            <stroke android:width="2dp" android:color="#FF335C"/>
        </shape>
    </item>
    <item>
        <shape>
            <solid android:color="#232323"/>
            <corners android:radius="28dp"/>
            <stroke android:width="1dp" android:color="#333333"/>
        </shape>
    </item>
</selector>''', encoding='utf-8')

# El elemento completo recibe el foco; los hijos no lo interceptan.
p = res / 'layout/list_stream_item.xml'
s = p.read_text(encoding='utf-8')
s = s.replace(
    'android:background="@drawable/premium_card" android:clickable="true" android:focusable="true"',
    'android:background="@drawable/premium_card" android:clickable="true" '
    'android:focusable="true" android:focusableInTouchMode="false" '
    'android:descendantFocusability="blocksDescendants"',
)
p.write_text(s, encoding='utf-8')

# La búsqueda de Inicio es un control de primera clase para mando y teclado.
p = res / 'layout/fragment_main.xml'
s = p.read_text(encoding='utf-8')
s = s.replace(
    'android:gravity="center_vertical" android:paddingStart="18dp"',
    'android:gravity="center_vertical" android:clickable="true" android:focusable="true" '
    'android:focusableInTouchMode="false" android:paddingStart="18dp"',
    1,
)
p.write_text(s, encoding='utf-8')

# Layout específico para Android TV / Google TV. Conserva la misma lógica, pero aumenta
# objetivos de foco, tipografía y miniaturas para lectura a distancia.
tv_layout = res / 'layout-television'
tv_layout.mkdir(parents=True, exist_ok=True)
(tv_layout / 'fragment_main.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#0F0F0F">

    <LinearLayout
        android:id="@+id/premium_home_header"
        android:layout_width="match_parent"
        android:layout_height="92dp"
        android:layout_alignParentTop="true"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:paddingStart="32dp"
        android:paddingEnd="32dp">

        <TextView
            android:id="@+id/premium_search_button"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:background="@drawable/premium_search_bar"
            android:clickable="true"
            android:drawableStart="@drawable/ic_search"
            android:drawablePadding="14dp"
            android:focusable="true"
            android:focusableInTouchMode="false"
            android:gravity="center_vertical"
            android:paddingStart="24dp"
            android:paddingEnd="24dp"
            android:text="Buscar videos, canales y más"
            android:textColor="#E0E0E0"
            android:textSize="20sp"/>
    </LinearLayout>

    <org.schabi.newpipe.views.ScrollableTabLayout
        android:id="@+id/main_tab_layout"
        android:layout_width="match_parent"
        android:layout_height="82dp"
        android:layout_alignParentBottom="true"
        android:background="#0F0F0F"
        app:tabGravity="fill"
        app:tabIndicatorColor="#FF0033"
        app:tabIndicatorGravity="top"
        app:tabIndicatorHeight="3dp"
        app:tabMinWidth="120dp"
        app:tabMode="fixed"
        app:tabRippleColor="#33FF0033"
        app:tabTextColor="#BDBDBD"
        app:tabSelectedTextColor="#FF0033"/>

    <androidx.viewpager.widget.ViewPager
        android:id="@+id/pager"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/premium_home_header"
        android:layout_above="@id/main_tab_layout"/>
</RelativeLayout>''', encoding='utf-8')

(tv_layout / 'list_stream_item.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/itemRoot"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginStart="28dp"
    android:layout_marginEnd="28dp"
    android:layout_marginTop="8dp"
    android:layout_marginBottom="8dp"
    android:background="@drawable/premium_card"
    android:clickable="true"
    android:focusable="true"
    android:focusableInTouchMode="false"
    android:descendantFocusability="blocksDescendants"
    android:padding="12dp">

    <ImageView
        android:id="@+id/itemThumbnailView"
        android:layout_width="250dp"
        android:layout_height="140dp"
        android:background="@drawable/premium_thumbnail"
        android:clipToOutline="true"
        android:scaleType="centerCrop"
        android:src="@drawable/placeholder_thumbnail_video"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"/>

    <org.schabi.newpipe.views.NewPipeTextView
        android:id="@+id/itemDurationView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginEnd="7dp"
        android:layout_marginBottom="7dp"
        android:background="@drawable/premium_duration"
        android:paddingHorizontal="7dp"
        android:paddingVertical="3dp"
        android:textColor="#FFFFFF"
        android:textSize="14sp"
        app:layout_constraintBottom_toBottomOf="@id/itemThumbnailView"
        app:layout_constraintEnd_toEndOf="@id/itemThumbnailView"
        tools:text="12:34"/>

    <org.schabi.newpipe.views.NewPipeTextView
        android:id="@+id/itemVideoTitleView"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="18dp"
        android:ellipsize="end"
        android:maxLines="2"
        android:textColor="#FFFFFF"
        android:textSize="22sp"
        android:textStyle="bold"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toEndOf="@id/itemThumbnailView"
        app:layout_constraintTop_toTopOf="@id/itemThumbnailView"
        tools:text="Título del video"/>

    <org.schabi.newpipe.views.NewPipeTextView
        android:id="@+id/itemUploaderView"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:ellipsize="end"
        android:lines="1"
        android:textColor="#D0D0D0"
        android:textSize="18sp"
        app:layout_constraintEnd_toEndOf="@id/itemVideoTitleView"
        app:layout_constraintStart_toStartOf="@id/itemVideoTitleView"
        app:layout_constraintTop_toBottomOf="@id/itemVideoTitleView"
        tools:text="Canal"/>

    <org.schabi.newpipe.views.NewPipeTextView
        android:id="@+id/itemAdditionalDetails"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:ellipsize="end"
        android:lines="1"
        android:textColor="#AFAFAF"
        android:textSize="16sp"
        app:layout_constraintBottom_toBottomOf="@id/itemThumbnailView"
        app:layout_constraintEnd_toEndOf="@id/itemVideoTitleView"
        app:layout_constraintStart_toStartOf="@id/itemVideoTitleView"
        tools:text="620 K vistas • hace 3 días"/>

    <org.schabi.newpipe.views.AnimatedProgressBar
        android:id="@+id/itemProgressView"
        style="@style/Widget.AppCompat.ProgressBar.Horizontal"
        android:layout_width="0dp"
        android:layout_height="4dp"
        android:progressDrawable="?progress_horizontal_drawable"
        app:layout_constraintBottom_toBottomOf="@id/itemThumbnailView"
        app:layout_constraintEnd_toEndOf="@id/itemThumbnailView"
        app:layout_constraintStart_toStartOf="@id/itemThumbnailView"/>
</androidx.constraintlayout.widget.ConstraintLayout>''', encoding='utf-8')

# Banner propio para Android TV (el manifest base ya apunta a newpipe_tv_banner).
for folder in res.glob('mipmap-*'):
    for banner in folder.glob('newpipe_tv_banner.*'):
        banner.unlink()
mip = res / 'mipmap-anydpi'
mip.mkdir(parents=True, exist_ok=True)
(mip / 'newpipe_tv_banner.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <shape>
            <solid android:color="#0F0F0F"/>
            <corners android:radius="16dp"/>
            <stroke android:width="2dp" android:color="#242424"/>
        </shape>
    </item>
    <item
        android:width="116dp"
        android:height="116dp"
        android:gravity="center"
        android:drawable="@drawable/ic_miyoutube_brand"/>
</layer-list>''', encoding='utf-8')

# Navegación D-pad: en modo TV, la búsqueda recibe foco inicial y cada pestaña
# se vuelve focalizable; al enfocar una pestaña se selecciona automáticamente.
p = root / 'app/src/main/java/org/schabi/newpipe/fragments/MainFragment.java'
s = p.read_text(encoding='utf-8')
s = s.replace('        setupTabs();', '        setupTabs();\n        configureUniversalTvNavigation();', 1)
marker = '    private void updateTabLayoutPosition() {'
method = '''    private void configureUniversalTvNavigation() {\n        final Object uiModeService = requireContext().getSystemService(\n                android.content.Context.UI_MODE_SERVICE);\n        final boolean isTelevision = uiModeService instanceof android.app.UiModeManager\n                && ((android.app.UiModeManager) uiModeService).getCurrentModeType()\n                == android.content.res.Configuration.UI_MODE_TYPE_TELEVISION;\n        if (!isTelevision) {\n            return;\n        }\n\n        binding.premiumSearchButton.setFocusable(true);\n        binding.premiumSearchButton.setFocusableInTouchMode(false);\n        binding.premiumSearchButton.setOnKeyListener((view, keyCode, event) -> {\n            if (event.getAction() == android.view.KeyEvent.ACTION_DOWN\n                    && (keyCode == android.view.KeyEvent.KEYCODE_DPAD_CENTER\n                    || keyCode == android.view.KeyEvent.KEYCODE_ENTER)) {\n                view.performClick();\n                return true;\n            }\n            return false;\n        });\n\n        final android.view.View tabStripCandidate = binding.mainTabLayout.getChildAt(0);\n        if (tabStripCandidate instanceof android.view.ViewGroup) {\n            final android.view.ViewGroup tabStrip =\n                    (android.view.ViewGroup) tabStripCandidate;\n            for (int index = 0; index < tabStrip.getChildCount(); index++) {\n                final int tabIndex = index;\n                final android.view.View tabView = tabStrip.getChildAt(index);\n                tabView.setFocusable(true);\n                tabView.setFocusableInTouchMode(false);\n                tabView.setOnFocusChangeListener((view, hasFocus) -> {\n                    if (hasFocus && tabIndex < binding.mainTabLayout.getTabCount()) {\n                        final com.google.android.material.tabs.TabLayout.Tab tab =\n                                binding.mainTabLayout.getTabAt(tabIndex);\n                        if (tab != null) {\n                            tab.select();\n                        }\n                    }\n                });\n            }\n        }\n\n        binding.premiumSearchButton.post(binding.premiumSearchButton::requestFocus);\n    }\n\n'''
if marker not in s:
    raise RuntimeError('No se encontró updateTabLayoutPosition en MainFragment')
s = s.replace(marker, method + marker, 1)
p.write_text(s, encoding='utf-8')

(root / 'MI-YOUTUBE-NOTICE.txt').write_text('''Mi YouTube 1.3.1 Universal\nBasado en TeamNewPipe/NewPipe v0.29.0 y NewPipeExtractor.\nLicencia GPL-3.0-or-later.\nInterfaz premium oscura adaptable a celular, tablet, TV Box, Android TV y Google TV.\nIncluye foco visible para D-pad, búsqueda focalizable, navegación de pestañas por control remoto,\nlayout de televisión con objetivos grandes y banner propio Mi YouTube.\nNo es una aplicación oficial de YouTube ni de NewPipe.\n''', encoding='utf-8')

print('Mi YouTube 1.3.1 Universal personalizado')
