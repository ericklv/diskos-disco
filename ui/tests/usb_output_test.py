#!/usr/bin/env python3
"""Exercise the production output state machine with controlled IPC and ALSA fixtures."""
import subprocess
import tempfile
from pathlib import Path
ui = Path(__file__).resolve().parents[1]
src = (ui / 'modes.c').read_text()
block = src.split('/* OUTPUT-ROUTE-BEGIN */', 1)[1].split('/* OUTPUT-ROUTE-END */', 1)[0]
c = r'''
#define _GNU_SOURCE
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <glob.h>
#include <unistd.h>
#include <sys/stat.h>
typedef struct lv_timer_t { int unused; } lv_timer_t;
typedef struct {int have_track;char path[256];long position_ms;} track_state_t;
enum { OUT_INTERNAL, OUT_SPDIF, OUT_USB };
static char root[128],card[256],pcm[256],idpath[300],playpath[300],subpath[350],usbstatus[400];
#define OUT_USB_CARD card
#define OUT_PCM_GLOB pcm
static uint32_t now=1000;static unsigned gen=1;
static int playing,cfg_spdif,sends,fail_at,fail_all,fail_from,resumes,seeks,refreshes;
static char commands[256][32],toast[160];static const char *blocked;
static track_state_t state={1,"/track.flac",42000};
static lv_timer_t *lv_timer_create(void(*cb)(lv_timer_t*),unsigned period,void*u){(void)cb;(void)period;(void)u;return calloc(1,sizeof(lv_timer_t));}
static void lv_timer_del(lv_timer_t*t){free(t);}
static uint32_t lv_tick_get(void){return now;}
static uint32_t lv_tick_elaps(uint32_t t){return now-t;}
static unsigned ipc_generation(void){return gen;}
static int ipc_is_ready(void){return 1;}
static void ipc_get_state(track_state_t*out){*out=state;}
static int ui_is_playing(void){return playing;}
static int ipc_send_cmd(const char*cmd){
 assert(sends<256);snprintf(commands[sends++],32,"%s",cmd);
 if((fail_at&&sends==fail_at)||fail_all||(fail_from&&sends>=fail_from))return -1;
 if(!strcmp(cmd,"0201000C0000")){playing=!playing;resumes++;}
 if(!strncmp(cmd,"0666",4))playing=0;
 return 0;
}
static int ui_seek_to(long ms){extern int modes_output_busy(void);assert(!modes_output_busy());assert(ms==42000);seeks++;return 0;}
static int simple_cfg_get_int(const char*k,int d){(void)k;(void)d;return cfg_spdif;}
static void simple_cfg_set_int(const char*k,int v){(void)k;cfg_spdif=v;}
static const char *ui_output_blocked(void){return blocked;}
static void ui_toast(const char*t){snprintf(toast,sizeof toast,"%s",t);}
static int test_usleep(unsigned n){assert(n==65000);return 0;}
#define usleep test_usleep
int modes_output_route(void);
''' + block + r'''
static void modes_ui_refresh(void){refreshes++;}
static void status_text(const char*t){FILE*f=fopen(pcm,"w");assert(f);fputs(t,f);fclose(f);}
static void device(int on){
 if(on){FILE*f=fopen(idpath,"w");assert(f);fputs("1234:abcd\n",f);fclose(f);assert(mkdir(playpath,0700)==0||access(playpath,F_OK)==0);assert(mkdir(subpath,0700)==0||access(subpath,F_OK)==0);f=fopen(usbstatus,"w");assert(f);fputs("closed\n",f);fclose(f);}
 else{unlink(idpath);unlink(usbstatus);rmdir(subpath);rmdir(playpath);}
}
static void reset(void){
 if(g_osw.tm)lv_timer_del(g_osw.tm);out_rec_clear();memset(&g_osw,0,sizeof g_osw);
 now=1000;gen=1;g_out_gen=1;g_out_route=OUT_INTERNAL;playing=0;cfg_spdif=0;
 sends=fail_at=fail_all=fail_from=resumes=seeks=refreshes=0;blocked=NULL;toast[0]=0;
 state=(track_state_t){1,"/track.flac",42000};status_text("closed\n");device(0);
}
static void ticks(int ms){for(int i=0;i<ms;i+=100){now+=100;if(g_osw.tm)osw_tick(g_osw.tm);else if(g_rec)out_recover_tick(g_rec_tm);}}
static void start_usb(void){assert(modes_output_mode_switch(OUT_USB)==0);ticks(700);assert(g_osw.usb_wait&&modes_output_busy());}
static void connect_usb(void){start_usb();device(1);ticks(700);assert(modes_output_route()==OUT_USB&&!modes_output_busy());}
int main(void){
 snprintf(root,sizeof root,"/tmp/diskos-usb-output-XXXXXX");assert(mkdtemp(root));
 snprintf(card,sizeof card,"%s/card1",root);assert(!mkdir(card,0700));
 snprintf(pcm,sizeof pcm,"%s/status",root);snprintf(idpath,sizeof idpath,"%s/usbid",card);snprintf(playpath,sizeof playpath,"%s/pcm0p",card);snprintf(subpath,sizeof subpath,"%s/sub0",playpath);snprintf(usbstatus,sizeof usbstatus,"%s/status",subpath);
 reset();playing=1;start_usb();assert(!playing&&resumes==1&&modes_output_route()==OUT_INTERNAL);
 assert(!strcmp(commands[1],"0666000C0003")&&!strcmp(commands[2],"0642000C0005")&&!strcmp(commands[3],"0657000C0008"));
 device(1);ticks(300);assert(modes_output_busy()&&!playing);device(0);ticks(100);device(1);ticks(600);
 assert(!modes_output_busy()&&modes_output_route()==OUT_USB&&playing&&seeks==1&&resumes==2);
 puts("PASS: host requested before enumeration, stable readiness before resume, intermittent device restarts hold");
 reset();playing=1;start_usb();ticks(8800);assert(!modes_output_busy()&&modes_output_route()==OUT_INTERNAL&&playing&&strstr(toast,"restored"));
 puts("PASS: missing-DAC timeout fully restores headphones before resuming");
 reset();playing=1;start_usb();fail_all=1;ticks(8800);assert(g_rec&&modes_output_busy()&&!playing&&strstr(toast,"restoring"));
 fail_all=0;ticks(1000);assert(!g_rec&&modes_output_route()==OUT_INTERNAL&&playing);
 puts("PASS: failed timeout restore stays recovering; success is announced only after complete retry");
 reset();connect_usb();device(0);g_rec=1;modes_usb_poll();assert(!g_osw.tm);g_rec=0;modes_usb_poll();assert(g_osw.tm);ticks(700);assert(modes_output_route()==OUT_INTERNAL&&!modes_output_busy());
 puts("PASS: unplug while busy retries after busy clears");
 reset();connect_usb();device(0);blocked="busy";modes_usb_poll();assert(modes_output_route()==OUT_USB&&!g_osw.tm);blocked=NULL;modes_usb_poll();assert(g_osw.tm);ticks(700);assert(modes_output_route()==OUT_INTERNAL);
 puts("PASS: blocked unplug restore preserves route and retries instead of claiming headphones");
 reset();connect_usb();device(0);fail_at=sends+1;modes_usb_poll();ticks(700);assert(modes_output_route()==OUT_USB&&!strstr(toast,"restored"));fail_at=0;modes_usb_poll();ticks(700);assert(modes_output_route()==OUT_INTERNAL);
 puts("PASS: rejected fallback command never overwrites USB state; subsequent poll retries");
 reset();start_usb();device(1);gen++;ticks(100);assert(!modes_output_busy()&&modes_output_route()==OUT_INTERNAL&&!playing);
 reset();playing=1;start_usb();device(1);snprintf(state.path,sizeof state.path,"/other.flac");ticks(700);assert(!playing&&seeks==0&&strstr(toast,"press play"));
 puts("PASS: player restart and track change cannot resume stale playback");
 reset();status_text("state: RUNNING\n");assert(modes_output_mode_switch(OUT_USB)<0&&sends==0);
 status_text("garbage\n");assert(modes_output_mode_switch(OUT_USB)<0&&sends==0);
 status_text("closed\n");device(1);assert(out_usb_card_ok());unlink(usbstatus);rmdir(subpath);rmdir(playpath);assert(!out_usb_card_ok());
 FILE*f=fopen(idpath,"w");assert(f);fputs("not-a-usb-id\n",f);fclose(f);mkdir(playpath,0700);assert(!out_usb_card_ok());
 device(1);FILE*usb=fopen(usbstatus,"w");assert(usb);fputs("state: DISCONNECTED\n",usb);fclose(usb);assert(!out_usb_card_ok());
 usb=fopen(usbstatus,"w");assert(usb);fputs("state: RUNNING\n",usb);fclose(usb);assert(out_usb_card_ok());
 puts("PASS: live/unknown PCM, malformed identity and input-only devices fail closed");
 reset();connect_usb();assert(modes_output_mode_switch(OUT_INTERNAL)==0);ticks(700);assert(modes_output_route()==OUT_INTERNAL&&!modes_output_busy());
 assert(!strcmp(commands[3],"0666000C0003")&&!strcmp(commands[4],"0657000C0008"));
 assert(!strcmp(commands[5],"0666000C0006")&&!strcmp(commands[6],"0642000C0000")&&!strcmp(commands[7],"0657000C0008"));
 reset();playing=1;assert(modes_output_mode_switch(OUT_USB)==0);assert(modes_output_mode_switch(OUT_INTERNAL)<0);ticks(300);gen++;ticks(100);assert(!playing&&!modes_output_busy());
 puts("PASS: explicit return clears host request; concurrent switch and restart during pause are isolated");
 for(int frame=1;frame<=3;frame++){
  reset();fail_at=frame;assert(modes_output_mode_switch(OUT_USB)==0);ticks(700);
  assert(!modes_output_busy()&&modes_output_route()==OUT_INTERNAL);
 }
 reset();fail_from=2;assert(modes_output_mode_switch(OUT_USB)==0);ticks(700);assert(g_rec&&modes_output_busy());fail_from=0;ticks(1000);assert(!modes_output_busy()&&modes_output_route()==OUT_INTERNAL);
 for(int frame=1;frame<=2;frame++){
  reset();start_usb();device(1);fail_at=sends+frame;ticks(700);assert(!modes_output_busy()&&modes_output_route()==OUT_INTERNAL);
 }
 reset();start_usb();status_text("state: RUNNING\n");int sent=sends;ticks(9000);assert(g_rec&&modes_output_busy()&&sends==sent);
 status_text("closed\n");ticks(700);assert(!modes_output_busy()&&modes_output_route()==OUT_INTERNAL);
 puts("PASS: timeout recovery will not reinitialise a live or unknown PCM; it waits for proven quiet");
 puts("PASS: every host-entry/rebind frame failure restores internal; repeated restore failure remains pending");
 reset();device(0);unlink(pcm);rmdir(card);rmdir(root);return 0;
}
'''
with tempfile.TemporaryDirectory() as td:
    p=Path(td);(p/'test.c').write_text(c)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-Wno-misleading-indentation',str(p/'test.c'),'-o',str(p/'test')],check=True)
    subprocess.run([str(p/'test')],check=True)
