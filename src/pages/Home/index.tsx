import Donation from "../../components/Home/Donation";
import HeaderSlider from "../../components/Home/HeaderSlider";
import Leaders from "../../components/Home/Leaders";
import NewGames from "../../components/Home/NewGames";
import Subscribes from "../../components/Home/Subscribes";
import Container from "../../components/common/Container";
import Navigation from "../../components/common/Navigation";
import { useGetCategoryProductsQuery } from "../../services/productsApi";

export default function Home() {

    const { data = [] } = useGetCategoryProductsQuery({})


    return (
        <Container>
            <Navigation />
            <HeaderSlider data={data.offers} />
            <NewGames data={data.new} />
            <Subscribes psSubs={data.psPlus} eaSubs={data.eaPlay} />
            <Leaders data={data.leaders} />
            <Donation data={data.donations} />
        </Container>
    )
}
