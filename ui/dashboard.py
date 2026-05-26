"""
Dashboard Page - Phase 9 リアルタイム反映対応
"""
import streamlit as st
from video_asset_manualize.asset_indexer import AssetIndexer
from video_asset_manualize.review_repository import ReviewRepository

def show_dashboard():
    st.header("📊 Dashboard")
    st.markdown("VideoAsset Manualize のプロジェクト全体概要です。")
    
    if st.button("🔄 リアルタイム更新", use_container_width=True):
        st.rerun()
    
    st.divider()
    
    try:
        indexer = AssetIndexer()
        review_repo = ReviewRepository()
        assets = indexer.scan_assets()
        booklets = indexer.scan_booklets()
        
        total_assets = len(assets)
        all_reviews = review_repo.list_all_reviews()
        approved_assets = sum(1 for r in all_reviews.values() if r.get('state') == 'approved')
        total_booklets = len(booklets)
        
        st.subheader("📈 統計情報")
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.metric("📦 生成済みアセット", total_assets)
        with metric_cols[1]:
            st.metric("✅ 承認済みアセット", approved_assets)
        with metric_cols[2]:
            st.metric("📚 生成済み冊子", total_booklets)
        with metric_cols[3]:
            approval_rate = int((approved_assets/total_assets)*100) if total_assets > 0 else 0
            st.metric("📊 承認率", f"{approval_rate}%")
        
        st.divider()
        
        st.subheader("⏰ 最近のアセット")
        if assets:
            recent_assets = sorted(assets, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
            for asset in recent_assets:
                aid = asset.get("asset_id", "unknown")
                title = asset.get("title", "Untitled")
                created = asset.get("created_at", "unknown")
                review = review_repo.get_review_state(aid)
                status = review if review else "draft"
                
                badge = "✅ Approved" if status == "approved" else ("🔄 In Review" if status == "in_review" else ("❌ Rejected" if status == "rejected" else "📝 Draft"))
                color = "🟢" if status == "approved" else ("🟡" if status == "in_review" else ("🔴" if status == "rejected" else "⚪"))
                
                st.write(f"{color} **{title}** (`{aid}`) - {badge}")
                st.caption(f"作成: {created}")
        else:
            st.info("📭 まだアセットが生成されていません。")
        
        st.divider()
        
        st.subheader("📚 最近の冊子")
        if booklets:
            recent_booklets = sorted(booklets, key=lambda x: x.get("created_at", ""), reverse=True)[:3]
            for b in recent_booklets:
                bid = b.get("project_id", "unknown")
                title = b.get("title", "Untitled")
                created = b.get("created_at", "unknown")
                count = len(b.get("assets", []))
                st.write(f"📖 **{title}** (`{bid}`) - {count} アセット")
                st.caption(f"作成: {created}")
        else:
            st.info("📭 まだ冊子が生成されていません。")
        
        st.divider()
        
        st.subheader("🚀 クイックスタート")
        quick_cols = st.columns(3)
        with quick_cols[0]:
            st.markdown("**📹 Single Video**\n1. 動画ファイルを指定\n2. Provider を選択\n3. Process Video で実行")
        with quick_cols[1]:
            st.markdown("**✅ Assets**\n1. 生成済みアセット一覧\n2. レビュー状態を変更\n3. コメントを保存")
        with quick_cols[2]:
            st.markdown("**📚 Batch & Booklet**\n1. Manifest JSON を指定\n2. Batch Build または Booklet Build\n3. 冊子を生成")
        
        st.divider()
        
        with st.expander("ℹ️ システム情報", expanded=False):
            st.write("**Phase**: Phase 9 (UI 実処理統合)")
            st.write("**Assets Directory**: output/exports")
            st.write("**Reviews Directory**: data/reviews")
            st.write(f"**Total Assets**: {total_assets}")
            st.write(f"**Total Booklets**: {total_booklets}")
    
    except Exception as e:
        st.error(f"❌ ダッシュボード読み込みエラー: {str(e)}")
        st.markdown("**対策**:\n- output/exports ディレクトリが存在するか確認\n- Single Video で動画を処理してアセットを生成")
