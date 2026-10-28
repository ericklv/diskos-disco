/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Copyright (C) 2026 diskOS contributors */
#ifndef NPSHADE_H
#define NPSHADE_H
int  npshade_style(void);    /* Display > QS style: 1 = "Shade" (now playing first, then Quick settings), 0 = "Classic" */
int  npshade_active(void);   /* the shade is on screen */
void npshade_open(void);     /* the first pull: the now-playing shade */
void npshade_close(void);
void npshade_grow(void);     /* the second pull: on to Quick settings */
void npshade_dismiss(void);  /* gone at once */
#endif
