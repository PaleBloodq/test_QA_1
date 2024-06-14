import React from "react";
import { Link } from "react-router-dom";
import { replaceUrl } from "../../../helpers/replaceUrl";
import { ProductType } from "../../../types/ProductType";

const DonationCard = React.memo(({ donation }: { donation: ProductType }) => {


    return (
        <>
            <Link to={'/donation/' + donation?.id} className='w-full h-[240px] flex flex-col items-start justify-between'>
                <img className='h-full rounded-xl mb-[18px]' src={replaceUrl(donation?.publications[0]?.product_page_image)} alt="donation image" />
            </Link>
        </>
    );
});

export default DonationCard;