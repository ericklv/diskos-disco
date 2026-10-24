#include "braun.h"
/* A-Z wheel design studies. Host preview only; no device behaviour changes. */
static lv_obj_t *azd_text(lv_obj_t *parent,const char *text,const lv_font_t *font,
                         lv_color_t color,int cx,int cy,int width){
    lv_obj_t *o=lv_label_create(parent);lv_label_set_text(o,text);kit_keep(o);
    lv_obj_set_style_text_font(o,font,0);lv_obj_set_style_text_color(o,color,0);
    lv_obj_set_style_text_align(o,LV_TEXT_ALIGN_CENTER,0);
    lv_obj_set_size(o,width,lv_font_get_line_height(font)+4);
    lv_obj_set_pos(o,cx-width/2,cy-(lv_font_get_line_height(font)+4)/2);
    lv_obj_remove_flag(o,LV_OBJ_FLAG_CLICKABLE);return o;
}
static lv_obj_t *azd_arc(lv_obj_t *parent,int radius,int width,lv_color_t color,
                        int opacity,int start,int end){
    lv_obj_t *o=lv_arc_create(parent);lv_obj_remove_style_all(o);kit_keep(o);
    lv_obj_set_size(o,radius*2,radius*2);lv_obj_set_pos(o,180-radius,180-radius);
    lv_arc_set_bg_angles(o,start,end);lv_arc_set_angles(o,0,0);
    lv_obj_set_style_arc_width(o,width,LV_PART_MAIN);
    lv_obj_set_style_arc_color(o,color,LV_PART_MAIN);
    lv_obj_set_style_arc_opa(o,opacity,LV_PART_MAIN);
    lv_obj_set_style_arc_rounded(o,1,LV_PART_MAIN);
    lv_obj_set_style_arc_opa(o,0,LV_PART_INDICATOR);
    lv_obj_remove_flag(o,LV_OBJ_FLAG_CLICKABLE|LV_OBJ_FLAG_SCROLLABLE);return o;
}
static lv_obj_t *azd_plate(lv_obj_t *parent,int x,int y,int w,int h,int radius,
                          lv_color_t color,int opacity){
    lv_obj_t *o=lv_obj_create(parent);lv_obj_remove_style_all(o);kit_keep(o);
    lv_obj_set_pos(o,x,y);lv_obj_set_size(o,w,h);lv_obj_set_style_radius(o,radius,0);
    lv_obj_set_style_bg_color(o,color,0);lv_obj_set_style_bg_opa(o,opacity,0);
    lv_obj_remove_flag(o,LV_OBJ_FLAG_CLICKABLE|LV_OBJ_FLAG_SCROLLABLE);return o;
}
static const lv_font_t *azd_font(int big){
    if(th_braun())return br_font(big?56:18,0);
    if(th_null())return big?TF(UI_36):TF(UI_16);
    if(th_zune()){
        LV_FONT_DECLARE(font_zune_light_50)
        LV_FONT_DECLARE(font_zune_regular_19)
        return big?&font_zune_light_50:&font_zune_regular_19;
    }
    return big?TF(UI_40):TF(UI_18);
}
static void azd_preview(lv_obj_t *parent,int design){
    for(int size=0;size<2;size++)for(int i=0;i<27;i++){
        uint32_t letter="ABCDEFGHIJKLMNOPQRSTUVWXYZ#"[i];if(th_zune()&&letter!='#')letter+=32;
        lv_font_glyph_dsc_t glyph;
        assert(lv_font_get_glyph_dsc(azd_font(size),&glyph,letter,0));
    }
    const lv_color_t surface=TC(SURFACE),raised=TC(SURFACE_RAISED),accent=TC(ACCENT_PRIMARY);
    const lv_color_t text=TC(TEXT_PRIMARY),muted=TC(TEXT_SECONDARY);
    lv_obj_t *ov=azd_plate(parent,0,0,360,360,0,TC(CANVAS),design==2?246:238);
    /* Static soft annulus edges: bounded LVGL arcs, no blur or frame-time texture work. */
    if(design==1){
        for(int j=0;j<7;j++)azd_arc(ov,160-j,52-2*j,surface,22+10*j,0,360);
        azd_arc(ov,153,40,surface,255,0,360);
        azd_arc(ov,155,1,TC(OUTLINE_BRIGHT),28,205,330);
        azd_arc(ov,112,1,TC(BORDER_STRONG),60,0,360);
    }else if(design==2){
        azd_arc(ov,151,2,TC(BORDER),110,0,360);
        azd_arc(ov,151,2,accent,220,252,288);
        for(int j=0;j<5;j++)azd_arc(ov,158-j,15-2*j,accent,8+6*j,255,285);
        azd_arc(ov,112,1,TC(BORDER),60,0,360);
    }else{
        lv_obj_t *plate=azd_plate(ov,22,22,316,316,LV_RADIUS_CIRCLE,surface,255);
        lv_obj_set_style_bg_color(plate,raised,0);lv_obj_set_style_bg_grad_color(plate,surface,0);
        lv_obj_set_style_bg_grad_dir(plate,LV_GRAD_DIR_VER,0);
        lv_obj_set_style_border_width(plate,1,0);lv_obj_set_style_border_color(plate,TC(BORDER),0);
        lv_obj_set_style_border_opa(plate,100,0);
        azd_arc(ov,156,1,TC(OUTLINE_BRIGHT),35,205,335);
        azd_arc(ov,112,1,TC(BORDER),90,0,360);
        for(int j=0;j<27;j++){
            int degrees=(270+j*360/27)%360;
            azd_arc(ov,149,j%3==0?4:2,TC(TEXT_MUTED),70,degrees,degrees+1);
        }
    }
    for(int i=0;i<27;i++){
        int delta=(i-12+27)%27;if(delta>13)delta-=27;
        float deg=-90+(design==2?delta:i)*360.0f/27;
        float angle=deg*3.14159265f/180;
        int r=design==3?129:134,cx=180+(int)lroundf(r*cosf(angle)),cy=180+(int)lroundf(r*sinf(angle));
        if(i==12){
            int size=design==2?34:30;
            lv_obj_t *selection=azd_plate(ov,cx-size/2,cy-size/2,size,size,th_null()?3:design==3?9:LV_RADIUS_CIRCLE,accent,255);
            if(design!=3){lv_obj_set_style_shadow_color(selection,accent,0);lv_obj_set_style_shadow_width(selection,design==2?14:8,0);lv_obj_set_style_shadow_opa(selection,35,0);}
        }
        char letter[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ#"[i],0};
        if(th_zune()&&letter[0]!='#')letter[0]+=32;
        lv_obj_t *label=azd_text(ov,letter,azd_font(0),i==12?TC(ON_ACCENT):muted,cx,cy,28);
        if(design==2&&i!=12)lv_obj_set_style_text_opa(label,abs(delta)<4?245:abs(delta)<8?170:110,0);
    }
    if(design==1){
        lv_obj_t *hub=azd_plate(ov,132,132,96,96,th_null()?10:LV_RADIUS_CIRCLE,raised,255);
        lv_obj_set_style_bg_grad_color(hub,surface,0);lv_obj_set_style_bg_grad_dir(hub,LV_GRAD_DIR_VER,0);
        lv_obj_set_style_border_width(hub,1,0);lv_obj_set_style_border_color(hub,accent,0);lv_obj_set_style_border_opa(hub,110,0);
        lv_obj_set_style_shadow_color(hub,TC(FIXED_MEDIA_BLACK),0);lv_obj_set_style_shadow_width(hub,16,0);lv_obj_set_style_shadow_opa(hub,35,0);
        azd_text(ov,th_zune()?"m":"M",azd_font(1),text,180,180,90);
        azd_text(ov,th_zune()?"jump to":"JUMP TO",TF(UI_12),muted,180,110,150);
        azd_text(ov,th_zune()?"tap to jump":"TAP TO JUMP",TF(UI_12),muted,180,250,170);
    }else if(design==2){
        azd_text(ov,th_zune()?"jump to":"JUMP TO",TF(UI_12),muted,180,110,150);
        azd_text(ov,th_zune()?"m":"M",azd_font(1),text,180,174,140);
        azd_text(ov,th_zune()?"tap to jump":"TAP TO JUMP",TF(UI_12),accent,180,234,170);
        lv_obj_t *line=azd_plate(ov,164,260,32,2,1,accent,100);(void)line;
    }else{
        azd_text(ov,th_zune()?"jump to":"JUMP TO",TF(UI_12),muted,180,113,150);
        lv_obj_t *hub=azd_plate(ov,143,143,74,74,th_null()?5:22,accent,255);
        lv_obj_set_style_border_width(hub,1,0);lv_obj_set_style_border_color(hub,TC(OUTLINE_BRIGHT),0);lv_obj_set_style_border_opa(hub,55,0);
        azd_text(ov,th_zune()?"m":"M",th_null()?TF(UI_28):TF(UI_32),TC(ON_ACCENT),180,180,66);
        azd_text(ov,th_zune()?"l":"L",azd_font(0),muted,113,180,32);
        azd_text(ov,th_zune()?"n":"N",azd_font(0),muted,247,180,32);
        azd_text(ov,th_zune()?"tap to jump":"TAP TO JUMP",TF(UI_12),muted,180,249,170);
    }
}
