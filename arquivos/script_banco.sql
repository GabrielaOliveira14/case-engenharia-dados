
----------------------------------------------

drop table dim_usuarios;
drop table dim_nomes;
drop table dim_paises;
drop table fato;


CREATE TABLE dim_usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  genero VARCHAR, 
  idade INT, 
  id_nome INT, 
  id_pais INT, 
  CONSTRAINT FK_nome FOREIGN KEY (id_nome) REFERENCES dim_nomes(id), 
  CONSTRAINT FK_pais FOREIGN KEY (id_pais) REFERENCES dim_paises(id)
);


CREATE TABLE dim_nomes (
  id INTEGER PRIMARY KEY,
  nome VARCHAR
);



CREATE TABLE dim_paises (
  id INTEGER PRIMARY KEY, 
  nome VARCHAR
);


CREATE TABLE fato (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  Qtd_name_repetido INT, 
  Qtd_male INT, 
  Qtd_female INT, 
  Qtd_female_50_mais INT, 
  Qtd_male_50_mais INT, 
  id_nome INT, 
  id_pais INT, 
  CONSTRAINT FK_nome FOREIGN KEY (id_nome) REFERENCES dim_usuarios(id_nome),
  CONSTRAINT FK_pais FOREIGN KEY (id_pais) REFERENCES dim_usuarios(id_pais)
);



DELETE FROM fato;

INSERT INTO fato(Qtd_name_repetido, Qtd_male, Qtd_female, Qtd_female_50_mais, Qtd_male_50_mais, id_nome, id_pais) 
SELECT 
  COUNT(dn.nome) AS Qtd_name_repetido, 
  Sum(CASE WHEN du.genero = 'male' THEN 1 ELSE 0 END) AS Qtd_male, 
  Sum(CASE WHEN du.genero = 'female' THEN 1 ELSE 0 END) AS Qtd_female, 
  Sum(CASE WHEN du.idade > 50 AND du.genero = 'female' THEN 1 ELSE 0 END) AS Qtd_female_50_mais, 
  Sum(CASE WHEN du.idade > 50 AND du.genero = 'male' THEN 1 ELSE 0 END) AS Qtd_male_50_mais, 
  du.id_nome, 
  du.id_pais 
FROM 
  dim_usuarios du 
  INNER JOIN dim_nomes dn ON du.id_nome = dn.id 
  INNER JOIN dim_paises dp ON du.id_pais = dp.id 
GROUP BY  
  dp.nome, 
  dn.nome;

 

--- respostas

-- 1. Total de pessoas com o mesmo nome por país
SELECT 
  dp.nome AS Pais, 
  dn.nome AS Nome, 
  Qtd_name_repetido 
FROM 
  fato f 
  INNER JOIN dim_nomes dn ON dn.id = f.id_nome 
  INNER JOIN dim_paises dp ON dp.id = f.id_pais 
GROUP BY 
  dp.nome, 
  dn.nome
ORDER BY Qtd_name_repetido DESC;


-- 2. Distribuição de pessoas por gênero por país
SELECT 
  dp.nome AS Pais, 
  sum(Qtd_male) AS Qtd_male, 
  sum(Qtd_female) AS Qtd_female 
FROM 
  fato f 
  INNER JOIN dim_nomes dn ON dn.id = f.id_nome 
  INNER JOIN dim_paises dp ON dp.id = f.id_pais 
GROUP BY 
  dp.nome;


-- 3. Quantas pessoas da distribuição do ítem 2 possuí + de 50
SELECT 
  dp.nome AS Pais, 
  sum(Qtd_male_50_mais) AS Qtd_male_50_mais, 
  sum(Qtd_female_50_mais) AS Qtd_female_50_mais 
FROM 
  fato f 
  INNER JOIN dim_nomes dn ON dn.id = f.id_nome 
  INNER JOIN dim_paises dp ON dp.id = f.id_pais 
GROUP BY 
  dp.nome;
  
 
 
 
----------------------------------------------
