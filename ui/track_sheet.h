/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Shared Stats-inspired track actions. Kept header-only for existing build lists. */
#ifndef DISCO_TRACK_SHEET_H
#define DISCO_TRACK_SHEET_H
#include "theme_kit.h"
#include "curvelist.h"
static void track_sheet_text(lv_obj_t *p,const char *text,int x,int y,int w,const lv_font_t *font,lv_color_t color){
    lv_obj_t *l=lv_label_create(p);kit_keep(l);lv_label_set_text(l,text?text:"");
    lv_obj_set_pos(l,x,y);lv_obj_set_width(l,w);lv_obj_set_height(l,LV_SIZE_CONTENT);
    lv_label_set_long_mode(l,LV_LABEL_LONG_SCROLL_CIRCULAR);
    lv_obj_set_style_text_font(l,font,0);lv_obj_set_style_text_color(l,color,0);
    lv_obj_remove_flag(l,LV_OBJ_FLAG_CLICKABLE);
}
static void track_sheet_build(lv_obj_t *root,const char *title,const char *artist,
                              const void *cover,const char *const *names,const char *const *icons,
                              int count,lv_event_cb_t action,lv_event_cb_t back){
    lv_obj_set_style_bg_color(root,TC(CANVAS),0);lv_obj_set_style_bg_opa(root,255,0);
    lv_obj_remove_flag(root,LV_OBJ_FLAG_SCROLLABLE);
    LV_FONT_DECLARE(font_theme_20)
    extern lv_obj_t *kit_default_header(lv_obj_t*,const char*,lv_event_cb_t);
    if(th_null())kit_default_header(root,"Track",back);else ui_header_cb(root,"Track",back);
    lv_obj_t *tile=lv_obj_create(root);lv_obj_remove_style_all(tile);kit_keep(tile);
    lv_obj_set_pos(tile,76,69);lv_obj_set_size(tile,48,48);
    lv_obj_set_style_bg_color(tile,TC(SURFACE),0);lv_obj_set_style_bg_opa(tile,255,0);
    lv_obj_remove_flag(tile,LV_OBJ_FLAG_CLICKABLE|LV_OBJ_FLAG_SCROLLABLE);
    if(cover){lv_obj_t *im=lv_image_create(tile);lv_image_set_src(im,cover);lv_obj_center(im);
        const lv_image_dsc_t *d=cover;if(d->header.w)lv_image_set_scale(im,256*48/d->header.w);
    }else track_sheet_text(tile,LV_SYMBOL_AUDIO,12,12,28,TF(UI_24),TC(ACCENT_PRIMARY));
    track_sheet_text(root,title,127,70,161,th_null()?TF(UI_14):TF(UI_20),TC(TEXT_PRIMARY));
    track_sheet_text(root,artist,127,98,161,TF(UI_14),TC(TEXT_MUTED));
    lv_obj_t *list=lv_obj_create(root);lv_obj_remove_style_all(list);kit_keep(list);
    lv_obj_set_pos(list,53,127);lv_obj_set_size(list,254,181);
    lv_obj_set_flex_flow(list,LV_FLEX_FLOW_COLUMN);lv_obj_set_style_pad_row(list,6,0);
    lv_obj_set_style_pad_bottom(list,28,0);lv_obj_set_scroll_dir(list,LV_DIR_VER);
    lv_obj_set_scrollbar_mode(list,LV_SCROLLBAR_MODE_OFF);lv_obj_add_flag(list,LV_OBJ_FLAG_SCROLL_MOMENTUM);
    static curvelist_t curve;curvelist_attach(&curve,list,root,244);
    for(int k=0;k<count;k++){
        lv_obj_t *row=lv_obj_create(list);lv_obj_remove_style_all(row);kit_keep(row);
        lv_obj_set_size(row,244,43);lv_obj_set_flex_grow(row,0);
        lv_obj_set_style_radius(row,th_null()?0:21,0);
        lv_obj_set_style_bg_color(row,TC(SURFACE),0);lv_obj_set_style_bg_opa(row,255,0);
        lv_obj_add_flag(row,LV_OBJ_FLAG_CLICKABLE);lv_obj_remove_flag(row,LV_OBJ_FLAG_SCROLLABLE);
        lv_obj_set_style_bg_color(row,TC(SURFACE_PRESSED),LV_STATE_PRESSED);
        lv_obj_add_event_cb(row,action,LV_EVENT_CLICKED,(void*)(intptr_t)k);
        track_sheet_text(row,icons[k],11,12,27,k==0?&font_theme_20:TF(UI_18),TC(ACCENT_PRIMARY));
        track_sheet_text(row,names[k],43,11,187,th_null()?TF(UI_14):TF(UI_18),TC(TEXT_PRIMARY));
    }
    track_sheet_text(root,LV_SYMBOL_DOWN,165,318,30,TF(UI_16),TC(ACCENT_PRIMARY));
}
#endif
