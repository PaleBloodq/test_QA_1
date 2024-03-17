import { RootState } from "../../store/store";

export const selectedPublicationSelector = (state: RootState) =>
  state.publication.selectedPublication;
