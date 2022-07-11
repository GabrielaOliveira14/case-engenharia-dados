repeteadNamesByCountries = """
            SELECT 
                dp.nome AS Pais, 
                dn.nome AS Nome, 
                Qtd_name_repetido 
            FROM fato f 
            INNER JOIN dim_nomes dn ON dn.id = f.id_nome 
            INNER JOIN dim_paises dp ON dp.id = f.id_pais 
            GROUP BY dp.nome, dn.nome
            ORDER BY Qtd_name_repetido DESC;
        """

genderByCountry = """
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
        """

genderByCountryWith50YearsOld = """
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
        """
