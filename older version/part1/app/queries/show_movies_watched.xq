module namespace funcs = "com.funcs.my.index";

declare function funcs:show_movies_watched() as text()*
{
  for $b in doc("streamData")/root/row[type="Movie"]
  order by $b/valuation descending
  return $b/watched/text()
};