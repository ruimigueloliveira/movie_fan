module namespace funcs = "com.funcs.my.index";

declare function funcs:return_shows_watched() as text()*
{
  for $b in doc("streamData")/root/row
  order by $b/valuation descending
  return $b/watched/text()
};