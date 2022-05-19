module namespace funcs = "com.funcs.my.index";

declare function funcs:show_movies_rating() as text()*
{
  for $b in doc("streamData")/root/row[type="Movie"]
  order by $b/valuation descending
  return if (exists($b/valuation))
  then $b/valuation/text()
  else $b/valuation = "0"
};