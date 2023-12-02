" reds:
/red<Enter>gg0qrnhh13<c-x>nq373@r

" blue:
/blue<Enter>gg0qbnhh14<c-x>nq292@b

" green
/green<Enter>gg0qgnhh15<c-x>nq389@g

" text cleaning
:%s/Game //
:%g/ \d/d
:%s/:.*//
0ggj<c-v>GI+<Esc>100J

" calculate
yyi<c-r>=<c-r>"<Enter>
