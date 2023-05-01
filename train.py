from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, DPRQuestionEncoder, DPRQuestionEncoderTokenizer, Trainer
import argparse
import os
import shutil


parser = argparse.ArgumentParser()

parser.add_argument("-modeltype", "--model", help="please choose either multi or single.")
args = parser.parse_args()


def create_dpr(ctx, que):
    create_dir("DPR_Context")
    model = DPRContextEncoder.from_pretrained(ctx)
    tokenizer = DPRContextEncoderTokenizer.from_pretrained(ctx)
    tokenizer.save_pretrained("DPR/DPR_Context/Tokens")

    trainer_encoder = Trainer(model=model)
    trainer_encoder.save_model("DPR/DPR_Context")

    create_dir("DPR_Question")
    model = DPRQuestionEncoder.from_pretrained(que)
    tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(que)
    tokenizer.save_pretrained("DPR/DPR_Question/Tokens")

    trainer_encoder = Trainer(model=model)
    trainer_encoder.save_model("DPR/DPR_Question")


def create_dir(folder_name):
    dpr_path = "DPR"
    if os.path.exists(os.path.join(dpr_path, folder_name)):
        shutil.rmtree(os.path.join(dpr_path, folder_name))
    os.mkdir(os.path.join(dpr_path, folder_name))


if not args.model == "multi" or args.model == "single":
    raise KeyError("please choose either 'multi' or 'single.'") 
else:
    if args.model == "multi":
        model_ctx = "facebook/dpr-ctx_encoder-multiset-base"
        model_que = "facebook/dpr-question_encoder-multiset-base"
        create_dpr(model_ctx, model_que)

    elif args.model == "single":
        model_ctx = "facebook/dpr-question_encoder-single-nq-base"
        model_que = "facebook/dpr-ctx_encoder-single-nq-base"
        create_dpr(model_ctx, model_que)


