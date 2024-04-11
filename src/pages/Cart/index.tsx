import { useDispatch, useSelector } from "react-redux";
import Container from "../../components/common/Container";
import { cartSelector } from "../../features/Cart/cartSelectors";
import Tag from "../../components/common/Tag";
import { getDiscount } from "../../hooks/getDiscount";
import { deleteFromCart } from "../../features/Cart/cartSlice";
import { CartItemType } from "../../types/cartItem";

export default function Cart() {

    const { items } = useSelector(cartSelector)
    const dispatch = useDispatch()


    return (
        <Container>
            <h1 className="text-header">Корзина</h1>
            <div className="mt-7 flex flex-col gap-2 w-full">
                {items.map((item: CartItemType) => {
                    return (
                        <div className="custom-border p-2 flex justify-between w-full h-[90px]">
                            <img className="w-[111px] object-cover rounded-xl" src={item.img} alt="img" />
                            <div className="flex flex-col justify-between items-start">
                                <h1 className="text-subtitle-info font-medium">{item.title}</h1>
                                <p className="text-subtitle">{item.publication} - {item.platform}</p>
                                <div className="flex gap-3">
                                    <h2 className="price-small">{item.discount ? getDiscount(item.price, item.discount) : item.price} ₽</h2>
                                    {item.discount && <Tag type="discount">-{item.discount}%</Tag>}
                                </div>
                            </div>
                            <button onClick={() => dispatch(deleteFromCart(item.id))} className="w-6 h-6 rounded-full flex items-center justify-center dark:bg-[#FFFFFF0D]">
                                <svg className="fill-[#606D7B] dark:fill-white" width="10" height="10" viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M0.827504 0.827748C1.03892 0.616337 1.38168 0.616337 1.59309 0.827748L4.99977 4.234L8.40645 0.827748C8.6016 0.632599 8.90867 0.617587 9.12104 0.782714L9.17204 0.827748C9.38345 1.03916 9.38345 1.38193 9.17204 1.59334L5.76579 5.00002L9.17204 8.4067C9.36719 8.60184 9.3822 8.90892 9.21708 9.12129L9.17204 9.17229C8.96063 9.3837 8.61786 9.3837 8.40645 9.17229L4.99977 5.76603L1.59309 9.17229C1.39794 9.36743 1.09087 9.38245 0.878504 9.21732L0.827504 9.17229C0.616093 8.96087 0.616093 8.61811 0.827504 8.4067L4.23376 5.00002L0.827504 1.59334C0.632355 1.39819 0.617343 1.09112 0.78247 0.878748L0.827504 0.827748Z" fillOpacity="0.6" />
                                </svg>
                            </button>
                        </div>
                    )
                })}
            </div>
        </Container>
    )
}
