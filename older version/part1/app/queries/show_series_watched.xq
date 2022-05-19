module namespace funcs = "com.funcs.my.index";

declare function funcs:show_series_watched() as text()*
{
  for $b in doc("streamData")/root/row[type="TV Show"]
  order by $b/valuation descending
  return $b/watched/text()
};