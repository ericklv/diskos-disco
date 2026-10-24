#!/usr/bin/env python3
"""Exercise the actual compiled circle-cache function against its original formula.
Requires a native `make -C ui CROSS= host-render` build.
"""
from pathlib import Path
import subprocess, tempfile
app=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='curve-cache-') as tmp:
 p=Path(tmp)
 (p/'probe.c').write_text(r'''
#include "curvelist.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
int main(void){
 int radii[]={150,172,180,100};
 for(int pass=0;pass<2;pass++)for(int i=0;i<4;i++)for(int d=-1;d<=radii[i]+5;d++){
  int r=radii[i],old=d<0||d>=r?0:(int)sqrtf((float)(r*r-d*d));
  assert(curvelist_circle_half(r,d)==old);
 }
 puts("PASS exact circle spans, cold/warm caches, boundaries and uncached-radius fallback");
}
''')
 subprocess.run(['gcc','-std=gnu11','-DLV_CONF_INCLUDE_SIMPLE','-I'+str(app),str(p/'probe.c'),str(app/'curvelist.o'),'-Wl,--gc-sections','-lm','-o',str(p/'probe')],check=True)
 subprocess.run([str(p/'probe')],check=True)
