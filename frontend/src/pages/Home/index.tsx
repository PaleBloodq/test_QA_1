import { useEffect } from "react";
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
import cookie from 'cookiejs';

export default function Home() {

    const { data = [] } = useGetCategoryProductsQuery({})

    function getTokenFromUrl(url) {
        const tokenRegex = /token=([^&#]+)/;
        const match = url.match(tokenRegex);
        console.log('match = ', match)

        if (match && match[1]) {
            return match[1];
        } else {
            return null;
        }
    }

    useEffect(() => {
        const newToken = getTokenFromUrl(window.location.href);
        console.log(newToken)
        if (newToken !== null) {
            cookie.set('token', newToken);
        }
        console.log(cookie.get('token'))
    }, [])


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
