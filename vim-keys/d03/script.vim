" Note: this approach is really slow because it involves running a macro (that
" switches between windows) >1000 times. Not sure why that's so slow, but
" there's certainly a better way to do this.

" add row and column of periods to top, left, and bottom
" (because otherwise the macro for search/yank becomes messed up?)
gg0
yyPVr.<c-v>GI.<esc>yyGpgg

" create a scratch buffer
:vsp
:enew
<c-w><c-w>
" search for numbers
/\d\+<Enter>
" move back to start of line
0

" create a macro that does the following:
" 1. n move to next occurrence of match
" 2. ma mark beginning of match
" 3. gn select entire match
" 4. ^V switch to block visual
" 5. okhojl move cursor to beginning of match and left and up one, then to end
" and down and right one. This will select a box 3 rows tall and X+2 columns
" wide (where X is the length of the number)
" 6. y`a copy the selected text and move back to mark
" 7. (unprintable characters):
"   <c-w><right arrow>  move right, to scratch buffer
"   p                   paste copied content
"   v`]                 select the text we just pasted (`] means "end of
"                       last-inserted text)
"   J                   Join all selected text into one line
"   o<Esc>              create a newline
"   <c-w><left arrow>   move back to original buffer
qqnmagn<c-v>okhojly`a<c-w><right>pv`]Jo<Esc><c-w><left>q

" run the maco 1226 more times (there are 1227 numbers in my input)
1226@q

" close the original buffer (your input file), leaving only the scratch buf
:q
" delete the blank line at the end
Gdd

" delete all lines which ONLY contain numbers and the '.' symbol
:%g/^[0-9. ]\+$/d
" delete everything but numbers and newlines
:%s/[^0-9]//g
" change newlines to "+"
:%s/\n/ + /
" write a 0 at the end of the line, because there's a trailing "+"
A0<Esc>

" copy the line, go into insert mode, then evaluate it
cc<c-r>=<c-r>"<Enter><Esc>
