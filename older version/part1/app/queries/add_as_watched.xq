module namespace funcs = "com.funcs.my.index";

declare updating function funcs:add_as_watched($show_id, $watched)
{
  let $bs := doc('streamData')//row
  for $y in $bs 
  where $y/show_id=$show_id
  return replace node $y/watched/text() with $watched
};