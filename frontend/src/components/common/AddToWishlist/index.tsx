import { useEffect, useState } from "react";
import { useAddToWishlistMutation, useDeleteFromWishlistMutation, useGetWishlistQuery } from "../../../services/userApi";

import { Bounce, Slide, ToastContainer, Zoom, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const icons = {
    standart: <svg className="w-6 h-6" viewBox="0 0 24 24" role="img" xmlns="http://www.w3.org/2000/svg" aria-labelledby="favouriteIconTitle" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none" color="#000000"><g id="SVGRepo_bgCarrier" strokeWidth="0"></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <title id="favouriteIconTitle">Favourite</title> <path d="M12,21 L10.55,19.7051771 C5.4,15.1242507 2,12.1029973 2,8.39509537 C2,5.37384196 4.42,3 7.5,3 C9.24,3 10.91,3.79455041 12,5.05013624 C13.09,3.79455041 14.76,3 16.5,3 C19.58,3 22,5.37384196 22,8.39509537 C22,12.1029973 18.6,15.1242507 13.45,19.7149864 L12,21 Z"></path> </g></svg>,
    active: <svg className="w-6 h-6" viewBox="0 0 24 24" role="img" xmlns="http://www.w3.org/2000/svg" aria-labelledby="favouriteIconTitle" stroke="#ff4242" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="#ff4242" color="#000000"><g id="SVGRepo_bgCarrier" strokeWidth="0"></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round" stroke="#CCCCCC" strokeWidth="0.144"></g><g id="SVGRepo_iconCarrier"> <title id="favouriteIconTitle">Favourite</title> <path d="M12,21 L10.55,19.7051771 C5.4,15.1242507 2,12.1029973 2,8.39509537 C2,5.37384196 4.42,3 7.5,3 C9.24,3 10.91,3.79455041 12,5.05013624 C13.09,3.79455041 14.76,3 16.5,3 C19.58,3 22,5.37384196 22,8.39509537 C22,12.1029973 18.6,15.1242507 13.45,19.7149864 L12,21 Z"></path> </g></svg>
};

export default function AddToWishlist({ id }) {
    const [addToWish] = useAddToWishlistMutation();
    const [deleteFromWish] = useDeleteFromWishlistMutation();
    const { data: wishListData, refetch } = useGetWishlistQuery({ id });
    const [activeIcon, setActiveIcon] = useState(icons.standart);
    const notify = () => toast('Бот уведомит о скидке');

    const inWishList = wishListData?.find((item) => item.id === id);

    useEffect(() => {
        if (wishListData) {
            if (inWishList) {
                setActiveIcon(icons.active);
            } else {
                setActiveIcon(icons.standart);
            }
        }
    }, [wishListData, inWishList]);

    async function handleWishlist() {
        if (inWishList) {
            await deleteFromWish(id);
        } else {
            await addToWish(id);
            notify()
        }
        refetch()
        setActiveIcon(inWishList ? icons.standart : icons.active);
    }

    return (
        <>
            <ToastContainer
                toastClassName="text-center !min-h-[30px] bg-opacity-20 bg-black backdrop-blur-sm rounded-2xl mt-5 w-10/12 mx-auto text-white font-bold border-solid border border-[#ffffff52]"
                position="top-center"
                autoClose={2000}
                hideProgressBar
                newestOnTop={false}
                closeButton={false}
                rtl={false}
                pauseOnFocusLoss={false}
                draggable={false}
                pauseOnHover
                theme="dark"
                transition={Slide}
            />
            <button onClick={handleWishlist} className="my-4 ml-auto flex items-center px-3 py-2 custom-border text-title-xl rounded-xl">
                {activeIcon}
            </button>
        </>
    );
}