function tableRow( items ) {
  const finalItems = items instanceof Array ? items : [ items ];
  const td = finalItems.reduce( ( memo, item ) => `${ memo }<td>${ item }</td>`, '' );

  return `<tr>${ td }</tr>`;
}

export default tableRow;
