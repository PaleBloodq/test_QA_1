import HeaderSlider from "../../components/Home/HeaderSlider";
import NewGames from "../../components/Home/NewGames";
import Container from "../../components/common/Container";
import Navigation from "../../components/common/Navigation";

export default function Home() {
    return (
        <Container>
            <Navigation />
            <HeaderSlider />
            <NewGames />
        </Container>
    )
}
