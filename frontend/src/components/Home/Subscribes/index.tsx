import { SectionType } from "../../../types/SectionType";
import EAPlay from "./EAPlay";
import PSPlus from "./PSPlus";

export default function Subscribes({ psSubs, eaSubs }: { psSubs: SectionType, eaSubs: SectionType }) {

    return (
        <div className="mt-7 flex flex-col gap-7">
            <PSPlus data={psSubs?.products} />
            <EAPlay data={eaSubs?.products} />
        </div>
    )
}
