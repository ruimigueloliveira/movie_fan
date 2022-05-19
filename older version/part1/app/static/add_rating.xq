(: onde está o row[4] é onde se deve inserir o id:)
(:chamei valuation em vez de rating pois alguns filmes já possuem um atributo chamado rating que devolve a restrição de idade para assistir:)

for $x in doc("streamData")//row[4]
return insert node <valuation>"10"</valuation> as first into $x