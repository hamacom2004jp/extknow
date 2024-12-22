from cmdbox.app import common, feature
from extknow.app import pgvector
from extknow import version
from pathlib import Path
from typing import Dict, Any, Tuple, Union, List
import argparse
import logging
import shutil


class PgvectorInstall(feature.Feature):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "pgvector"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'down'

    def get_option(self):
        """
        この機能のオプションを返します

        Returns:
            Dict[str, Any]: オプション
        """
        return dict(
            type="str", default=None, required=False, multi=False, hide=False, use_redis=self.USE_REDIS_FALSE,
            discription_ja="pgvectorのコンテナを停止します。",
            discription_en="Down the pgvector container.",
            choise=[
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
            dist_path = Path('pgvectordb')
            returncode, output, cmd = common.cmd(f"docker compose -f {dist_path}/docker-compose.yml down", logger, slise=-1)
            if returncode != 0:
                ret = dict(error=dict(cmd=cmd, msg=f"down error: {output}"))
                logger.error(f"down error: {output}, cmd: {cmd}")

            ret = dict(success=dict(cmd=cmd, msg=f"down success: {output}"))
            logger.info(f"down success: {output}, cmd: {cmd}")
        except Exception as e:
            logger.error(f"down error: {str(e)}")
            ret = dict(error=f"down error: {str(e)}")
        common.print_format(ret, args.format, tm, args.output_json, args.output_json_append, pf=pf)
        if 'success' not in ret:
            return 1, ret, None
        return 0, ret, None
