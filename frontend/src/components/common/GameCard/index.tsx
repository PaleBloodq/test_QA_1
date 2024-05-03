import { Link } from "react-router-dom";
import { ProductType } from "../../../types/ProductType";
import Tag from "../Tag";
import React from "react";
import { replaceUrl } from "../../../helpers/replaceUrl";

const GameCard = React.memo(({ game }: { game: ProductType }) => {


    return (
        <Link to={`/game/${game.id}/${game.publications[0].id}`} className='w-full h-full flex flex-col items-start justify-between'>
            <img className='rounded-xl max-h-[200px] mb-[18px]' src={replaceUrl(game.publications[0].preview)} alt="game image" />
            <h1 className='text-title text-start'>{game.title}</h1>
            {game.publications && <h2 className='text-subtitle'>{game.publications[0].title}</h2>}
            <div className='flex gap-2'>
                <h3 className='price-small'>
                    {game.publications[0].discount
                        ? game.publications[0].final_price
                        : game.publications[0].original_price} ₽
                </h3>
                {game.publications[0].discount !== null && <Tag type="discount">-{game.publications[0].discount}%</Tag>}
            </div>
        </Link>
    );
});
export default GameCard;