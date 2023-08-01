import { Column } from "react-table";
import tableDataCheck from "./tableDataCheck.json";

export const columnsDataCheck = [
  {
    Header: "NAME",
    accessor: "name",
  },
  {
    Header: "PROGRESS",
    accessor: "progress",
  },
  {
    Header: "QUANTITY",
    accessor: "quantity",
  },
  {
    Header: "DATE",
    accessor: "date",
  },
];
export const columnsDataComplex = [
  {
    Header: "IMAGE",
    accessor: "IMG_ID",
  },
  {
    Header: "DETECTED",
    accessor: "PRED_LAB",
  },
  {
    Header: "PREDICTION COUNT",
    accessor: "PRED_CT",
  },
  {
    Header: "MAP URL",
    accessor: "GEO_TAG_URL",
  },
  {
    Header: "MAIL SENT",
    accessor: "mail",
  },
  {
    Header: "DISTANCE (in km)",
    accessor: "coord",
  }
];

export type ColumnData = Column[];

export type TableData = Column<{
  IMG_ID: (string | boolean)[];
  GEO_TAG_URL: string;
  PRED_CT?: string;
  quantity?: number;
  PRED_LAB: number;
  mail: number;
  artworks?: string;
  rating?: number;
  coord?: string;
}>;

export type TableProps = {
  columnsData: ColumnData;
  tableData: TableData[];
  threshold: number;
};
