import { Link } from "react-router-dom";
import { GameType } from "../../../types/gameType";
import { getDiscount } from "../../../hooks/getDiscount";
import Tag from "../Tag";
import React from "react";

const GameCard = React.memo(({ game }: { game: GameType }) => {
    const { title, photoUrls, publications } = game;
    const { price, discount } = publications[0];

    return (
        <Link to={'/game/' + game.id} className='w-full h-full flex flex-col items-start justify-between'>
            <img className='rounded-xl max-h-[200px] mb-[18px]' src={photoUrls[0]} alt="game image" />
            <h1 className='text-title text-start'>{title}</h1>
            {publications && <h2 className='text-subtitle'>{publications[0].title}</h2>}
            <div className='flex gap-2'>
                <h3 className='price-small'>
                    {discount.percent && discount.percent > 0
                        ? getDiscount(price[0].price, discount.percent)
                        : price[0].price} ₽
                </h3>
                {discount.percent !== 0 &&
                    <Tag type="discount">-{discount.percent}%</Tag>}
            </div>
        </Link>
    );
});
export default GameCard;