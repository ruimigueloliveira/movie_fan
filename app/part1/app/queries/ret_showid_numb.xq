module namespace funcs = "com.funcs.my.index";

declare function funcs:ret_showid_numb()
{
  let $x := doc("streamData")//row[last()]
  return $x/show_id/text()
};