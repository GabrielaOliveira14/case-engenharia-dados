insertIntoFato = '''
            INSERT INTO fato(
              Qtd_name_repetido, Qtd_male, Qtd_female, 
              Qtd_female_50_mais, Qtd_male_50_mais, 
              id_nome, id_pais
            )
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
            GROUP BY dp.nome, dn.nome;
        '''

cleanFato = 'DELETE FROM fato;'

getDimNames = "SELECT * FROM dim_nomes"

getDimPais = "SELECT * FROM dim_paises"
