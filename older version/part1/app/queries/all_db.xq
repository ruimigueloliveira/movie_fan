module namespace funcs = "com.funcs.my.index";

declare function funcs:all_db() as element()*
{
  for $b in doc("streamData")/root/row
  return $b
};