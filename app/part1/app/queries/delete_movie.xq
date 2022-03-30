module namespace funcs = "com.funcs.my.index";

declare updating function funcs:delete_movie($id)
{
  for $x in doc("streamData")//row
  where $x/show_id = $id
  return delete node $x
};