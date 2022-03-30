module namespace funcs = "com.funcs.my.index";

declare updating function funcs:add_rating($id, $rating){
  for $x in doc("streamData")//row
  where $x/show_id = $id
  
  return if (exists($x/valuation))
  then replace node $x/valuation/text() with $rating
  else insert node <valuation>{$rating}</valuation> as last into $x
};
