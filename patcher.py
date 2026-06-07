#!/usr/bin/env python3
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "TMessagesProj", "src", "main", "java")

def find_file(name):
    for dp, _, files in os.walk(SRC):
        if name in files:
            return os.path.join(dp, name)
    return None

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def write(p, t):
    with open(p, "w", encoding="utf-8") as f: f.write(t)
    print(f"✔ {os.path.relpath(p, ROOT)}")

def patch_once(path, marker, insertion, before=False):
    text = read(path)
    if insertion.strip() in text:
        print(f"↩ skip {os.path.relpath(path, ROOT)}")
        return True
    if marker not in text:
        return False
    repl = (insertion + "\n" + marker) if before else (marker + "\n" + insertion)
    write(path, text.replace(marker, repl, 1))
    return True

ACTIVITY = '''\
package org.telegram.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.widget.LinearLayout;
import org.telegram.messenger.MessagesController;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.Cells.TextCheckCell;

public class WeryGramPremiumActivity extends BaseFragment {
    @Override
    public android.view.View createView(Context context) {
        actionBar.setBackButtonImage(org.telegram.messenger.R.drawable.ic_ab_back);
        actionBar.setTitle("WeryGram");
        actionBar.setActionBarMenuOnItemClick(new org.telegram.ui.ActionBar.ActionBar.ActionBarMenuOnItemClick() {
            @Override public void onItemClick(int id) { if (id == -1) finishFragment(); }
        });

        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));

        TextCheckCell premiumCell = new TextCheckCell(context);
        SharedPreferences prefs = MessagesController.getGlobalMainSettings();
        boolean isEnabled = prefs.getBoolean("wery_visual_premium", false);

        premiumCell.setTextAndValueAndCheck(
            "Visual Premium", 
            "Дает визуально телеграм премиум", 
            isEnabled, 
            false, 
            true
        );

        premiumCell.setOnClickListener(v -> {
            boolean newState = !prefs.getBoolean("wery_visual_premium", false);
            prefs.edit().putBoolean("wery_visual_premium", newState).apply();
            premiumCell.setChecked(newState);
        });

        root.addView(premiumCell);
        fragmentView = root;
        return fragmentView;
    }
}
'''

def main():
    print("▶ WeryGram patcher v3\n")
    
    # 1. ПАТЧИМ SETTINGS ACTIVITY И СОЗДАЕМ ЭКРАН
    sa = find_file("SettingsActivity.java")
    if sa:
        fill_anchors = [
            "void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {",
            "public void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {",
            "private void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {",
        ]
        fill_anchor = next((a for a in fill_anchors if a in read(sa)), None)
        if fill_anchor:
            patch_once(sa, fill_anchor, fill_anchor.replace("{", "{\n        items.add(0, UItem.asButton(1000, org.telegram.messenger.R.drawable.msg_settings, \"WeryGram\"));"))
            
            click_anchors = [
                "void onItemClick(UItem item, View view, int position, float x, float y) {",
                "public void onItemClick(UItem item, View view, int position, float x, float y) {",
                "private void onItemClick(UItem item, View view, int position, float x, float y) {",
                "void onClick(UItem item, View view, int position, float x, float y) {",
                "public void onClick(UItem item, View view, int position, float x, float y) {",
            ]
            click_anchor = next((a for a in click_anchors if a in read(sa)), None)
            if click_anchor:
                patch_once(sa, click_anchor, click_anchor.replace("{", "{\n        if (item != null && item.id == 1000) { presentFragment(new WeryGramPremiumActivity()); return; }"))

        dest = os.path.join(os.path.dirname(sa), "WeryGramPremiumActivity.java")
        with open(dest, "w", encoding="utf-8") as f: f.write(ACTIVITY)
        print("✔ created WeryGramPremiumActivity.java")

    # 2. АВТОМАТИЧЕСКИЙ ПАТЧ USERCONFIG ДЛЯ РАБОТЫ ПРЕМИУМА
    uc = find_file("UserConfig.java")
    if uc:
        uc_marker = "public boolean isPremium() {"
        uc_insert = "        if (org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean(\"wery_visual_premium\", false)) return true;"
        if not patch_once(uc, uc_marker, uc_insert, before=False):
            print("✘ UserConfig.java: public boolean isPremium() не найден!", file=sys.stderr)
        
    print("\n✅ Скрипт отработал. Запускай сборку (gradlew assembleDebug).")

if __name__ == "__main__":
    main()
    
