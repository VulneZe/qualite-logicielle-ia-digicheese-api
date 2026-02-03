import re

class Validator:

    @classmethod
    def validate_password(cls, plain_password: str) -> str :
        """
        Valide le mot de passe :
        - Minimum 12 caractères
        - Au moins 1 majuscule
        - Au moins 1 minuscule
        - Au moins 1 chiffre
        - Au moins 1 caractère spécial
        - Pas d'espaces
        """
        if plain_password is None:
            raise ValueError("Veuillez saisir un mot de passe")

        if not re.search(r"^(?=(.*[A-Z])+)(?=(.*[a-z])+)(?=(.*[\d])+)(?=.*\W)(?!.*\s).{12,}$", plain_password):
            raise ValueError("Le mot de passe doit contenir au moins douze caractères, un chiffre, une majuscule et un caractère spécial")
        return plain_password

    @classmethod
    def validate_email(cls, email: str) -> str:
        return email