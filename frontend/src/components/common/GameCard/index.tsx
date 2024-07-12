import { Link } from "react-router-dom";
import { ProductType } from "../../../types/ProductType";
import Tag from "../Tag";
import React from "react";
import { replaceUrl } from "../../../helpers/replaceUrl";
import { findCheapestPublication } from "../../../helpers/findCheapestPublication";

const GameCard = React.memo(({ game }: { game: ProductType }) => {

    const mainPublication = (game.publications.find((pub) => pub.is_main === true)) || findCheapestPublication(game.publications);


    return (
        <Link to={`/game/${game?.id}/${mainPublication?.id}`} className='w-full h-full flex flex-col items-start justify-between'>
            <img className='rounded-xl object-cover !h-[200px] w-full mb-[18px]' src={replaceUrl(mainPublication?.product_page_image)} alt="game image" />
            <h1 className='text-title text-start'>{game?.title}</h1>
            {game?.publications && <h2 className='text-subtitle'>{mainPublication?.title}</h2>}
            <div className='flex gap-2'>
                <h3 className='price-small'>
                    {mainPublication?.final_price} ₽
                </h3>
                {mainPublication && mainPublication?.discount !== 0 && <Tag type="discount">-{mainPublication?.discount}%</Tag>}
            </div>
        </Link>
    );
});
export default GameCard;