from flask import request

class DateHelper:
    """
    Classe utilitária para lidar com dados de formulários enviados via requsições HTTP.

    """

    def get_all_names_form(self):
        """
        Captura todos os dados enviados via formulário (método POST) e os converte em um dicionário.

        Returns:
            dict: Um dicionário contendo os campos e valores do formulário.
        """
        
        data = request.form.to_dict()
        return data