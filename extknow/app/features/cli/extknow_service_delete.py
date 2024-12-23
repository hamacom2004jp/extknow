from cmdbox.app import common, feature
from extknow.app import pgvector
from typing import Dict, Any, Tuple, Union, List
import argparse
import logging


class ServiceDelete(feature.Feature):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "service"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'selete'

    def get_option(self):
        """
        この機能のオプションを返します

        Returns:
            Dict[str, Any]: オプション
        """
        return dict(
            type="str", default=None, required=False, multi=False, hide=False, use_redis=self.USE_REDIS_FALSE,
            discription_ja="サービスを削除します。",
            discription_en="Delete the service.",
            choise=[
                dict(opt="dbhost", type="str", default="localhost", required=True, multi=False, hide=True, choise=None,
                        discription_ja="接続するデータベースホスト名を指定します。",
                        discription_en="Specify the database host name to connect to."),
                dict(opt="dbport", type="int", default=15432, required=True, multi=False, hide=True, choise=None,
                        discription_ja="接続するデータベースポートを指定します。",
                        discription_en="Specify the database port to connect to."),
                dict(opt="dbname", type="str", default="extknow", required=True, multi=False, hide=True, choise=None,
                        discription_ja="接続するデータベース名を指定します。",
                        discription_en="Specify the name of the database to connect to."),
                dict(opt="dbuser", type="str", default="postgres", required=True, multi=False, hide=True, choise=None,
                        discription_ja="接続するデータベースユーザー名を指定します。",
                        discription_en="Specifies the database user name to connect to."),
                dict(opt="dbpass", type="str", default="postgres", required=True, multi=False, hide=True, choise=None,
                        discription_ja="接続するデータベースパスワードを指定します。",
                        discription_en="Specify the database password to connect to."),
                dict(opt="dbtimeout", type="int", default=30, required=False, multi=False, hide=True, choise=None,
                        discription_ja="データベース接続のタイムアウトを指定します。",
                        discription_en="Specifies the database connection timeout."),
                dict(opt="servicename", type="str", default=None, required=False, multi=False, hide=False, choise=None,
                        discription_ja="サービス名を指定します。",
                        discription_en="Specify the service name."),
            ])

    def apprun(self, logger:logging.Logger, args:argparse.Namespace, tm:float, pf:List[Dict[str, float]]=[]) -> Tuple[int, Dict[str, Any], Any]:
        """
        この機能の実行を行います

        Args:
            logger (logging.Logger): ロガー
            args (argparse.Namespace): 引数
            tm (float): 実行開始時間
            pf (List[Dict[str, float]]): 呼出元のパフォーマンス情報

        Returns:
            Tuple[int, Dict[str, Any], Any]: 終了コード, 結果, オブジェクト
        """
        try:
            db = pgvector.Pgvector(
                logger=logger,
                dbhost=args.dbhost,
                dbport=args.dbport,
                dbname=args.dbname,
                dbuser=args.dbuser,
                dbpass=args.dbpass,
                dbtimeout=args.dbtimeout)
            db.delete_service(servicename=args.servicename)
            ret = dict(success="insert_service success.")
            logger.info(f"insert_service success. dbhost={args.dbhost}, dbport={args.dbport}, dbname={args.dbname}, dbuser={args.dbuser}, " + \
                        f"servicename={args.servicename}")
        except Exception as e:
            logger.error(f"insert_service error: {str(e)}. dbhost={args.dbhost}, dbport={args.dbport}, dbname={args.dbname}, dbuser={args.dbuser}, " + \
                         f"servicename={args.servicename}")
            ret = dict(error=f"insert_service error: {str(e)} dbhost={args.dbhost}, dbport={args.dbport}, dbname={args.dbname}, dbuser={args.dbuser}, " + \
                             f"servicename={args.servicename}")
        common.print_format(ret, args.format, tm, args.output_json, args.output_json_append, pf=pf)
        if 'success' not in ret:
            return 1, ret, None
        return 0, ret, None

