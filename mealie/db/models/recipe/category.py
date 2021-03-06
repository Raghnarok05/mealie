import sqlalchemy as sa
import sqlalchemy.orm as orm
from db.models.model_base import SqlAlchemyBase
from fastapi.logger import logger
from slugify import slugify
from sqlalchemy.orm import validates

recipes2categories = sa.Table(
    "recipes2categories",
    SqlAlchemyBase.metadata,
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey("recipes.id")),
    sa.Column("category_slug", sa.String, sa.ForeignKey("categories.slug")),
)


class Category(SqlAlchemyBase):
    __tablename__ = "categories"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, index=True, nullable=False)
    slug = sa.Column(sa.String, index=True, unique=True, nullable=False)
    recipes = orm.relationship(
        "RecipeModel", secondary=recipes2categories, back_populates="recipeCategory"
    )

    @validates("name")
    def validate_name(self, key, name):
        assert not name == ""
        return name

    def __init__(self, name) -> None:
        self.name = name.strip()
        self.slug = slugify(name)

    @staticmethod
    def create_if_not_exist(session, name: str = None):
        test_slug = slugify(name)
        try:
            result = session.query(Category).filter(Category.slug == test_slug).one()
            if result:
                logger.info("Category exists, associating recipe")
                return result
            else:
                logger.info("Category doesn't exists, creating tag")
                return Category(name=name)
        except:
            logger.info("Category doesn't exists, creating category")
            return Category(name=name)

    def to_str(self):
        return self.name

    def dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "recipes": [x.dict() for x in self.recipes],
        }

    def dict_no_recipes(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
        }
