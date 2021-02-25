module namespace funcs = "com.funcs.my.index";

declare function funcs:watched_by_country($country) as text()*
{
  for $b in doc("streamData")/root/row[contains(country,$country)]
  order by $b/title
  return $b/watched/text()
};
