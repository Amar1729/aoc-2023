" 12 red
" 13 green
" 14 blue
"
" decrement all red
"
/red<enter>
gg0
qr
  nhh
  13<c-x>
  n
q
" until you've gone through all reds (there were 374 in my input)
373@r

" same for blue
/blue
gg0
qb
  nhh
  14<c-x>
  n
q
292@b

" same for green
/green
gg0
qg
  nhh
  15<c-x>
  n
q
389@g

" delete 'Game '
:%s/Game //
" delete all lines that take too many dice
:%g/ \d/d

" delete everything but the game IDs
:%s/:.*//

" put a plus symbol preceding every line but the first
0ggj<c-v>GI+<Esc>

" join into one line
100J

" copy line, open calculator to eval it, paste it
yy
i<c-r>=
<c-r>"
<Enter>
