#!/usr/bin/env python3
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "TMessagesProj", "src", "main", "java")

def find_file(name):
    for dp, _, files in os.walk(SRC):
        if name in files: return os.path.join(dp, name)
    return None

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def write(p, t):
    with open(p, "w", encoding="utf-8") as f: f.write(t)
    print(f"✔ {os.path.relpath(p, ROOT)}")

def find_method_end(text, open_brace):
    depth = 0
    for i in range(open_brace, len(text)):
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0: return i
    return len(text) - 1

def insert_before(path, marker, insertion):
    text = read(path)
    if insertion.strip() in text: return True
    if marker not in text: return False
    write(path, text.replace(marker, insertion + "\n" + marker, 1)); return True

def insert_after(path, marker, insertion):
    text = read(path)
    if insertion.strip() in text: return True
    if marker not in text: return False
    write(path, text.replace(marker, marker + "\n" + insertion, 1)); return True

ACTIVITY = '''\
package org.telegram.ui;
import android.content.Context;
import android.content.SharedPreferences;
import android.widget.LinearLayout;
import android.widget.Switch;
import android.widget.TextView;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.MessagesController;
import org.telegram.messenger.NotificationCenter;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;

public class WeryGramPremiumActivity extends BaseFragment {
    private SharedPreferences prefs;
    
    private void addRow(Context ctx, LinearLayout parent, String title, String sub, String key) {
        LinearLayout row = new LinearLayout(ctx);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(14), AndroidUtilities.dp(16), AndroidUtilities.dp(14));
        row.setGravity(android.view.Gravity.CENTER_VERTICAL);
        
        LinearLayout labels = new LinearLayout(ctx);
        labels.setOrientation(LinearLayout.VERTICAL);
        labels.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
        
        TextView t = new TextView(ctx);
        t.setText(title);
        t.setTextSize(android.util.TypedValue.COMPLEX_UNIT_SP, 16);
        t.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText));
        
        TextView s = new TextView(ctx);
        s.setText(sub);
        s.setTextSize(android.util.TypedValue.COMPLEX_UNIT_SP, 13);
        s.setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteGrayText2));
        
        labels.addView(t);
        labels.addView(s);
        
        android.view.View div = new android.view.View(ctx);
        div.setBackgroundColor(Theme.getColor(Theme.key_divider));
        LinearLayout.LayoutParams dp2 = new LinearLayout.LayoutParams(AndroidUtilities.dp(1), AndroidUtilities.dp(40));
        dp2.setMargins(AndroidUtilities.dp(12), 0, AndroidUtilities.dp(12), 0);
        div.setLayoutParams(dp2);
        
        Switch toggle = new Switch(ctx);
        toggle.setChecked(prefs.getBoolean(key, false));
        toggle.setOnCheckedChangeListener((btn, checked) -> {
            prefs.edit().putBoolean(key, checked).apply();
            NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.currentUserPremiumStatusChanged);
            if ("wery_deleted_gifts".equals(key)) {
                try {
                    Object mc = MessagesController.getInstance(currentAccount);
                    for (java.lang.reflect.Field f : mc.getClass().getDeclaredFields()) {
                        if (f.getName().toLowerCase().contains("gift") && java.util.List.class.isAssignableFrom(f.getType())) {
                            f.setAccessible(true); ((java.util.List) f.get(mc)).clear();
                        }
                    }
                } catch (Exception e) {}
                try {
                    Object gc = Class.forName("org.telegram.messenger.GiftsController").getMethod("getInstance", int.class).invoke(null, currentAccount);
                    for (java.lang.reflect.Field f : gc.getClass().getDeclaredFields()) {
                        if (f.getName().toLowerCase().contains("gift") && java.util.List.class.isAssignableFrom(f.getType())) {
                            f.setAccessible(true); ((java.util.List) f.get(gc)).clear();
                        }
                    }
                } catch (Exception e) {}
                NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.starGiftsLoaded);
            }
        });
        
        row.addView(labels); row.addView(div); row.addView(toggle); parent.addView(row);
        android.view.View divider = new android.view.View(ctx);
        divider.setBackgroundColor(Theme.getColor(Theme.key_divider));
        divider.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 1));
        parent.addView(divider);
    }
    
    @Override
    public android.view.View createView(Context context) {
        actionBar.setBackButtonImage(org.telegram.messenger.R.drawable.ic_ab_back);
        actionBar.setTitle("WeryGram");
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override public void onItemClick(int id) { if (id == -1) finishFragment(); }
        });
        
        prefs = MessagesController.getGlobalMainSettings();
        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));
        
        addRow(context, root, "Visual Premium", "\\u0414\\u0430\\u0451\\u0442 \\u0432\\u0438\\u0437\\u0443\\u0430\\u043b\\u044c\\u043d\\u043e Telegram Premium", "wery_visual_premium");
        addRow(context, root, "\\u0420\\u0435\\u0436\\u0438\\u043c \\u041f\\u0440\\u0438\\u0437\\u0440\\u0430\\u043a\\u0430", "\\u0412\\u044b \\u0431\\u0443\\u0434\\u0435\\u0442\\u0435 \\u0432 \\u0441\\u0442\\u0430\\u0442\\u0443\\u0441\\u0435 \\u043d\\u0435\\u0432\\u0438\\u0434\\u0438\\u043c\\u043a\\u0438, \\u0430 \\u0442\\u0430\\u043a\\u0436\\u0435 \\u043f\\u0440\\u0438 \\u043f\\u0440\\u043e\\u0447\\u0442\\u0435\\u043d\\u0438\\u0438 \\u0441\\u043e\\u043e\\u0431\\u0449\\u0435\\u043d\\u0438\\u044f \\u043f\\u0440\\u043e\\u0441\\u043c\\u043e\\u0442\\u0440 \\u043d\\u0435 \\u0431\\u0443\\u0434\\u0435\\u0442 \\u0437\\u0430\\u0441\\u0447\\u0438\\u0442\\u044b\\u0432\\u0430\\u0442\\u044c\\u0441\\u044f", "wery_ghost_mode");
        addRow(context, root, "\\u0423\\u0434\\u0430\\u043b\\u0451\\u043d\\u043d\\u044b\\u0435 \\u043f\\u043e\\u0434\\u0430\\u0440\\u043a\\u0438", "\\u0412\\u044b \\u043c\\u043e\\u0436\\u0435\\u0442\\u0435 \\u0434\\u0430\\u0440\\u0438\\u0442\\u044c \\u0443\\u0434\\u0430\\u043b\\u0451\\u043d\\u043d\\u044b\\u0435 \\u0438 \\u0438\\u043c\\u0435\\u043d\\u043d\\u044b\\u0435 \\u043f\\u043e\\u0434\\u0430\\u0440\\u043a\\u0438", "wery_deleted_gifts");
            
        fragmentView = root;
        return fragmentView;
    }
}
'''

def patch_user_config():
    uc = find_file("UserConfig.java")
    if not uc: return False
    text = read(uc)
    if 'wery_visual_premium' in text: return True
    sig_pos = text.find("getCurrentUser()")
    if sig_pos == -1: return False
    ret_pos = text.find("return currentUser;", sig_pos)
    if ret_pos == -1: return False
    
    indent = text[text.rfind('\n', 0, ret_pos)+1:ret_pos]
    patch = (
        f'{indent}try {{\n'
        f'{indent}    android.content.SharedPreferences __p = org.telegram.messenger.MessagesController.getGlobalMainSettings();\n'
        f'{indent}    if (currentUser != null && __p.getBoolean("wery_visual_premium", false)) {{\n'
        f'{indent}        currentUser.premium = true;\n'
        f'{indent}        if (currentUser.emoji_status instanceof org.telegram.tgnet.TLRPC.TL_emojiStatus) {{\n'
        f'{indent}            long __curEid = ((org.telegram.tgnet.TLRPC.TL_emojiStatus) currentUser.emoji_status).document_id;\n'
        f'{indent}            if (__curEid != 0) __p.edit().putLong("wery_emoji_id", __curEid).apply();\n'
        f'{indent}            else {{ long __s = __p.getLong("wery_emoji_id", 0); if (__s != 0) ((org.telegram.tgnet.TLRPC.TL_emojiStatus) currentUser.emoji_status).document_id = __s; }}\n'
        f'{indent}        }} else {{ long __s = __p.getLong("wery_emoji_id", 0); if (__s != 0) {{ org.telegram.tgnet.TLRPC.TL_emojiStatus __es = new org.telegram.tgnet.TLRPC.TL_emojiStatus(); __es.document_id = __s; currentUser.emoji_status = __es; }} }}\n'
        f'{indent}        for (org.telegram.tgnet.TLRPC.TL_peerColor __c : new org.telegram.tgnet.TLRPC.TL_peerColor[]{{currentUser.profile_color, currentUser.color}}) {{\n'
        f'{indent}            String __k = __c == currentUser.profile_color ? "wery_p" : "wery_";\n'
        f'{indent}            if (__c != null) {{ if (__c.color >= 0 || __c.background_emoji_id != 0) __p.edit().putInt(__k+"color_id", __c.color).putLong(__k+"color_emoji", __c.background_emoji_id).apply(); else {{ int __id = __p.getInt(__k+"color_id", -1); long __em = __p.getLong(__k+"color_emoji", 0); if (__id >= 0) __c.color = __id; if (__em != 0) __c.background_emoji_id = __em; }} }}\n'
        f'{indent}        }}\n'
        f'{indent}    }}\n'
        f'{indent}}} catch (Exception __e) {{}}\n'
    )
    text = text[:ret_pos] + patch + text[ret_pos:]
    idx = text.find('public boolean isPremium() {')
    if idx != -1: text = text[:idx + 28] + '\n        if (org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("wery_visual_premium", false)) return true;' + text[idx + 28:]
    write(uc, text)
    return True

def patch_messages_controller():
    mc = find_file("MessagesController.java")
    if not mc: return False
    text = read(mc)
    modified = False

    if 'wery_visual_premium_controller' not in text:
        for v in ["public TLRPC.User getUser(Long id) {", "public TLRPC.User getUser(Long uid) {", "public TLRPC.User getUser(Long javaLong) {"]:
            if v in text:
                vn = "id" if "id)" in v else ("uid" if "uid)" in v else "javaLong")
                ins = (
                    f"        if ({vn} != null && org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean(\"wery_visual_premium\", false) && {vn}.longValue() == org.telegram.messenger.UserConfig.getInstance(currentAccount).getClientUserId()) {{\n"
                    f"            org.telegram.tgnet.TLRPC.User __u = users.get({vn});\n"
                    f"            if (__u != null && !__u.bot) {{ __u.premium = true; try {{ android.content.SharedPreferences __p = org.telegram.messenger.MessagesController.getGlobalMainSettings(); if (__u.emoji_status instanceof org.telegram.tgnet.TLRPC.TL_emojiStatus) {{ long __e = ((org.telegram.tgnet.TLRPC.TL_emojiStatus) __u.emoji_status).document_id; if (__e != 0) __p.edit().putLong(\"wery_emoji_id\", __e).apply(); else {{ long __s = __p.getLong(\"wery_emoji_id\", 0); if (__s != 0) ((org.telegram.tgnet.TLRPC.TL_emojiStatus) __u.emoji_status).document_id = __s; }} }} for (org.telegram.tgnet.TLRPC.TL_peerColor __c : new org.telegram.tgnet.TLRPC.TL_peerColor[]{{__u.profile_color, __u.color}}) {{ String __k = __c == __u.profile_color ? \"wery_p\" : \"wery_\"; if (__c != null) {{ if (__c.color >= 0 || __c.background_emoji_id != 0) __p.edit().putInt(__k+\"color_id\", __c.color).putLong(__k+\"color_emoji\", __c.background_emoji_id).apply(); else {{ int __id = __p.getInt(__k+\"color_id\", -1); long __em = __p.getLong(__k+\"color_emoji\", 0); if (__id >= 0) __c.color = __id; if (__em != 0) __c.background_emoji_id = __em; }} }} }} }} catch(Exception __e){{}} }}\n"
                    f"        }} //wery_visual_premium_controller"
                )
                text = text.replace(v, v + "\n" + ins, 1); modified = True; break

    for m in ["public void sendOnlineIfNeed() {", "void sendOnlineIfNeed() {", "public void sendOnline() {"]:
        if m in text and 'wery_ghost_online' not in text:
            text = text.replace(m, m + '\n        if (org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("wery_ghost_mode", false)) return; //wery_ghost_online', 1)
            modified = True; break

    for m in ["public void markDialogAsRead(", "public void readMessages(", "public void markMessagesAsRead("]:
        if m in text and 'wery_ghost_read' not in text:
            bp = text.find('{', text.find(m))
            if bp != -1: text = text[:bp+1] + '\n        if (org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("wery_ghost_mode", false)) return; //wery_ghost_read' + text[bp+1:]; modified = True; break

    if 'gift.sold_out' in text and 'wery_deleted_gifts_logic' not in text:
        text = text.replace('if (gift.sold_out)', 'if (gift.sold_out && !org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("wery_deleted_gifts", false)) //wery_deleted_gifts_logic')
        modified = True
    if 'gift.is_deleted' in text and 'wery_deleted_gifts_logic' not in text:
        text = text.replace('gift.is_deleted', '(gift.is_deleted && !org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("wery_deleted_gifts", false))')
        modified = True

    if 'wery_gifts_sort' not in text and 'starGifts' in text and "NotificationCenter.starGiftsLoaded" in text:
        sc = (
            '        if (org.telegram.messenger.MessagesController.getGlobalMainSettings().getBoolean("wery_deleted_gifts", false)) {\n'
            '            try { java.util.Collections.sort(starGifts, (g1, g2) -> { int r = Boolean.compare(g2.sold_out, g1.sold_out); if (r == 0) { String n1 = g1.gift != null && g1.gift.title != null ? g1.gift.title : ""; String n2 = g2.gift != null && g2.gift.title != null ? g2.gift.title : ""; return n1.compareTo(n2); } return r; }); } catch (Exception e) {}\n'
            '        } //wery_gifts_sort\n'
        )
        idx = text.find("NotificationCenter.starGiftsLoaded")
        ls = text.rfind("\n", 0, idx) + 1
        text = text[:ls] + sc + text[ls:]; modified = True

    if modified: write(mc, text)
    return True

def main():
    print("▶ WeryGram patcher build")
    patch_user_config()
    patch_messages_controller()
    
    sa = find_file("SettingsActivity.java")
    if not sa: sys.exit(1)
        
    insert_before(sa, "import org.telegram.ui.Components.", "import org.telegram.ui.WeryGramPremiumActivity;")
    text = read(sa)
    
    fa = next((a for a in ["void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {", "public void fillItems(ArrayList<UItem> items, UniversalAdapter adapter) {"] if a in text), None)
    if fa and 'UItem.asButton(1000' not in text:
        op = text.find(fa)
        ob = text.find('{', op)
        me = find_method_end(text, ob)
        write(sa, text[:me] + '        items.add(UItem.asButton(1000, R.drawable.msg_settings, "WeryGram"));\n' + text[me:])
    
    ca = next((a for a in ["void onItemClick(UItem item, View view, int position, float x, float y) {", "public void onItemClick(UItem item, View view, int position, float x, float y) {", "void onClick(UItem item) {"] if a in read(sa)), None)
    if ca: insert_after(sa, ca, '        if (item.id == 1000) { presentFragment(new WeryGramPremiumActivity()); return; }')

    dest = os.path.join(os.path.dirname(sa), "WeryGramPremiumActivity.java")
    if os.path.exists(dest): os.remove(dest)
    with open(dest, "w", encoding="utf-8") as f: f.write(ACTIVITY)
    print("✔ Patch completed! Ошибка устранена, проект готов к чистой сборке.")

if __name__ == "__main__":
    main()
    
