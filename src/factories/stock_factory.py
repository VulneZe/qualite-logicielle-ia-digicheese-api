from __future__ import annotations

from typing import List, Optional
from faker import Faker

from src.factories.interfaces.factories_interface import FactoriesInterface
from src.models.stock import Stock

fake = Faker()


class StockFactory(FactoriesInterface[Stock]):
    """
    StockFactory
    ------------
     créer facilement des objets Stock en base pendant les tests.
    """

    @classmethod
    def create_one(
        cls,
        session,
        designation: Optional[str] = None,
        **kwargs,
    ) -> Stock:
        """
        Crée 1 Stock, l'enregistre en DB (commit) et retourne l'objet rafraîchi.
        """
        stock = Stock(
            # designation est obligatoire dans StockBase :contentReference[oaicite:2]{index=2}
            designation=designation or f"Stock {fake.word()}",
            **kwargs,
        )

        session.add(stock)
        session.commit()
        session.refresh(stock)
        return stock

    @classmethod
    def create_many(
        cls,
        session,
        nb_stocks: int = 5,
        **kwargs,
    ) -> List[Stock]:
        """
        Crée plusieurs stocks.

        Exemple :
        stocks = StockFactory.create_many(session, nb_stocks=3)
        """
        stocks: List[Stock] = []
        for _ in range(nb_stocks):
            stocks.append(cls.create_one(session, **kwargs))
        return stocks
