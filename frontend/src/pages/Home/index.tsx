import { useDispatch, useSelector } from "react-redux";
import Donation from "../../components/Home/Donation";
import HeaderSlider from "../../components/Home/HeaderSlider";
import Leaders from "../../components/Home/Leaders";
import NewGames from "../../components/Home/NewGames";
import Other from "../../components/Home/Other";
import Subscribes from "../../components/Home/Subscribes";
import Container from "../../components/common/Container";
import Navigation from "../../components/common/Navigation";
import { useGetCategoryProductsQuery } from "../../services/productsApi";
import { SectionType } from "../../types/SectionType";
import { CartItemType } from "../../types/cartItem";
import { cartSelector } from "../../features/Cart/cartSelectors";
import { useEffect } from "react";
import { addToCart } from "../../features/Cart/cartSlice";

export default function Home() {

    const { data = [] } = useGetCategoryProductsQuery({})

    const dispatch = useDispatch()
    const { items }: { items: CartItemType[] } = useSelector(cartSelector)
    useEffect(() => {
        if (items.length > 0) {
            localStorage.setItem("storageCartItems", JSON.stringify(items))
        } else if (items.length === 0) {
            JSON.parse(localStorage.getItem('storageCartItems'))?.forEach((item: CartItemType) => {
                dispatch(addToCart(item))
            })
        }
    }, [items, dispatch])


    return (
        <Container>
            <Navigation />
            <HeaderSlider data={data.find((item: SectionType) => item.tag === "offers")} />
            <NewGames data={data.find((item: SectionType) => item.tag === "new")} />
            <Subscribes psSubs={data.find((item: SectionType) => item.tag === "psPlus")} eaSubs={data.find((item: SectionType) => item.tag === "eaPlay")} />
            <Leaders data={data.find((item: SectionType) => item.tag === "leaders")} />
            <Donation data={data.find((item: SectionType) => item.tag === "donation")} />
            <Other data={data.filter((item: SectionType) => item.tag === "other")} />
        </Container>
    )
}
