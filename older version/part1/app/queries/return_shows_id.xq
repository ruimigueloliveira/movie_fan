module namespace funcs = "com.funcs.my.index";

declare function funcs:return_shows_id() as text()*
{
  for $b in doc("streamData")/root/row
  order by $b/valuation descending
  return $b/show_id/text()
};