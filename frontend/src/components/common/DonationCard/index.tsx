import React from "react";
import { donationType } from "../../../types/donationType";
import { Link } from "react-router-dom";

const DonationCard = React.memo(({ donation }: { donation: donationType }) => {
    return (
        <Link to={'/donation/' + donation.id} className='w-full h-[240px] flex flex-col items-start justify-between'>
            <img className='h-full rounded-xl mb-[18px]' src={donation.photoUrls[0]} alt="donation image" />
        </Link>
    );
});

export default DonationCard;